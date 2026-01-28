# Copyright © 2026 Christopher C Berry All Rights Reserved.
# _______________________________________________
# GenerateVocabDeck.py
# Reads A1 vocabulary data from CSV, assigns stable GUIDs for decks and notes,
# updates the CSV in-place, and generates Anki .apkg decks grouped by category.

import os
import csv
import hashlib
import genanki


def stable_id(name: str) -> int:
    """
    Generate a stable numeric ID from a string using MD5.
    """
    digest = hashlib.md5(name.encode("utf-8"), usedforsecurity=False).hexdigest()
    return int(digest[:10], 16)


# ---------------------------------------------------------------------------
# Column indices (0-based)
# ---------------------------------------------------------------------------
COL_ITALIAN = 0
COL_ENGLISH = 1
COL_POS = 2
COL_IPA = 3
COL_GENDER = 4
COL_CONTEXT = 5
COL_SYNONYMS = 6
COL_EXAMPLE = 7
COL_EXAMPLE_EN = 8
COL_CATEGORY = 9
COL_DECK_NAME = 10
COL_DECK_GUID = 11
COL_NOTE_GUID = 12

NUM_COLUMNS = 13


def build_vocab_model() -> genanki.Model:
    """
    Build a genanki Model for Italian A1 vocabulary with two templates:
      - En->It  (front: English, back: everything else)
      - It->En  (front: Italian, back: everything else)
    """
    fields = [
        {"name": "Italian"},
        {"name": "English"},
        {"name": "PartOfSpeech"},
        {"name": "IPA"},
        {"name": "Gender"},
        {"name": "Context"},
        {"name": "Synonyms"},
        {"name": "ExampleIT"},
        {"name": "ExampleEN"},
        {"name": "Category"},
    ]

    # Shared block that shows all metadata
    info_block_en_it = """
    <div style="max-width:500px; margin:auto;">
    <div style="font-size:24px;">{{Italian}}</div><br><br>
    <b>Pronunciation:</b> {{IPA}}<br>
    <b>Part of Speech:</b> {{PartOfSpeech}}<br>
    <b>Gender:</b> {{Gender}}<br>
    <b>Context:</b> {{Context}}<br>
    {{#Synonyms}}<b>Synonyms:</b> {{Synonyms}}<br>{{/Synonyms}}
    <hr>
    <b>Example:</b> {{ExampleIT}}<br>
    <b>Translation:</b> {{ExampleEN}}<br>
    </div>
    """

    info_block_it_en = """
    <div style="max-width:500px; margin:auto;">
    <div style="font-size:24px;">{{English}}</div><br><br>
    <b>Pronunciation:</b> {{IPA}}<br>
    <b>Part of Speech:</b> {{PartOfSpeech}}<br>
    <b>Gender:</b> {{Gender}}<br>
    <b>Context:</b> {{Context}}<br>
    {{#Synonyms}}<b>Synonyms:</b> {{Synonyms}}<br>{{/Synonyms}}
    <hr>
    <b>Example:</b> {{ExampleIT}}<br>
    <b>Translation:</b> {{ExampleEN}}<br>
    </div>
        """

    templates = [
        {
            "name": "En->It",
            "qfmt": '<div style="font-size:24px;">{{English}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer">' + info_block_en_it,
        },
        {
            "name": "It->En",
            "qfmt": '<div style="font-size:24px;">{{Italian}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer">' + info_block_it_en,
        },
    ]

    model_name = "Words"
    model_id = stable_id(model_name)

    return genanki.Model(
        model_id,
        model_name,
        fields=fields,
        templates=templates,
        css="""
        .card { font-family: Arial; font-size: 18px; text-align: center; }
        """,
    )


def load_csv(csv_path: str):
    """Read the CSV and return (header, rows).  Rows are lists of strings."""
    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n").replace("\r", "\n")
    reader = csv.reader(content.strip().split("\n"))
    all_rows = list(reader)
    header = all_rows[0]
    data_rows = all_rows[1:]
    return header, data_rows


def save_csv(csv_path: str, header, rows):
    """Write header + rows back to the CSV."""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def ensure_guids(rows):
    """
    For every data row, ensure Deck Name, Deck GUID, and Note GUID are populated.
    Modifies rows in-place and returns the number of rows updated.
    """
    updated = 0
    for row in rows:
        # Pad row to NUM_COLUMNS if needed
        while len(row) < NUM_COLUMNS:
            row.append("")

        italian = row[COL_ITALIAN].strip()
        english = row[COL_ENGLISH].strip()
        category = row[COL_CATEGORY].strip()

        if not italian or not category:
            continue

        deck_name = f"Italian::A1::Vocab::{category}"
        deck_guid = str(stable_id(deck_name))
        note_guid = str(stable_id(f"{italian}"))

        changed = False
        if row[COL_DECK_NAME].strip() != deck_name:
            row[COL_DECK_NAME] = deck_name
            changed = True
        if row[COL_DECK_GUID].strip() != deck_guid:
            row[COL_DECK_GUID] = deck_guid
            changed = True
        if not row[COL_NOTE_GUID].strip():
            row[COL_NOTE_GUID] = note_guid
            changed = True

        if changed:
            updated += 1

    return updated


def generate_decks(rows, output_folder: str):
    """
    Group rows by deck name, create one .apkg per deck.
    """
    model = build_vocab_model()

    # Group by deck name
    deck_groups = {}
    for row in rows:
        if len(row) < NUM_COLUMNS:
            continue
        deck_name = row[COL_DECK_NAME].strip()
        if not deck_name:
            continue
        deck_groups.setdefault(deck_name, []).append(row)

    os.makedirs(output_folder, exist_ok=True)

    created = []
    for deck_name, group in sorted(deck_groups.items()):
        deck_guid = int(group[0][COL_DECK_GUID].strip())
        deck = genanki.Deck(deck_id=deck_guid, name=deck_name)

        notes_added = 0
        for row in group:
            note_guid = int(row[COL_NOTE_GUID].strip())
            fields = [
                row[COL_ITALIAN].strip(),
                row[COL_ENGLISH].strip(),
                row[COL_POS].strip(),
                row[COL_IPA].strip(),
                row[COL_GENDER].strip(),
                row[COL_CONTEXT].strip(),
                row[COL_SYNONYMS].strip(),
                row[COL_EXAMPLE].strip(),
                row[COL_EXAMPLE_EN].strip(),
                row[COL_CATEGORY].strip(),
            ]

            note = genanki.Note(guid=note_guid, model=model, fields=fields)
            deck.add_note(note)
            notes_added += 1

        # Derive filename from category
        category = deck_name.split("::")[-1]
        safe_category = category.replace(" ", "_").replace("&", "and")
        output_filename = f"A1_Vocab_{safe_category}.apkg"
        output_path = os.path.join(output_folder, output_filename)

        genanki.Package(deck).write_to_file(output_path)
        print(f"  Created {output_filename} ({notes_added} notes, deck: {deck_name})")
        created.append({"filename": output_filename, "deck_name": deck_name, "count": notes_added})

    return created


def main():
    csv_path = "A1_Vocab.csv"
    output_folder = "./Decks"

    print("Loading CSV...")
    header, rows = load_csv(csv_path)

    print("Ensuring GUIDs...")
    updated = ensure_guids(rows)
    print(f"  Updated {updated} rows with deck/note GUIDs.")

    print("Saving CSV...")
    save_csv(csv_path, header, rows)

    print("Generating Anki decks...")
    created = generate_decks(rows, output_folder)

    print(f"\n=== SUMMARY ===")
    print(f"Created {len(created)} deck files:")
    total_notes = 0
    for d in created:
        print(f"  {d['filename']} - {d['count']} notes ({d['deck_name']})")
        total_notes += d["count"]
    print(f"Total notes: {total_notes}")


if __name__ == "__main__":
    main()
