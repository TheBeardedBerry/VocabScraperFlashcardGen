# Copyright (C) 2026 Christopher C Berry All Rights Reserved.
# _______________________________________________
# GenerateVocabDeck.py
# Reads A1 vocabulary data from CSV, assigns stable GUIDs for decks and notes,
# updates the CSV in-place, and generates Anki .apkg decks grouped by category.

import argparse
import csv
import json
import os
from pathlib import Path

import genanki

from helpers import stable_id, load_csv, save_csv
from schemas import VOCAB_MODEL_FIELDS, VOCAB_MODEL_SEED, validate_vocab_row

TEMPLATE_DIR = Path(__file__).parent / "templates" / "vocab"


def _read_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def build_vocab_model() -> genanki.Model:
    """
    Build a genanki Model for Italian A1 vocabulary with two templates:
      - En->It  (front: English, back: everything else)
      - It->En  (front: Italian, back: everything else)
    """
    fields = [{"name": n} for n in VOCAB_MODEL_FIELDS]
    css = _read_template("card.css")

    templates = [
        {
            "name": "En->It",
            "qfmt": _read_template("en_it_front.html"),
            "afmt": _read_template("en_it_back.html"),
        },
        {
            "name": "It->En",
            "qfmt": _read_template("it_en_front.html"),
            "afmt": _read_template("it_en_back.html"),
        },
    ]

    model_id = stable_id(VOCAB_MODEL_SEED)

    return genanki.Model(
        model_id,
        VOCAB_MODEL_SEED,
        fields=fields,
        templates=templates,
        css=css,
    )


def load_vocab_csv(csv_path: str) -> list[dict]:
    """Read the vocab CSV using DictReader and return a list of row dicts."""
    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n").replace("\r", "\n")
    reader = csv.DictReader(content.strip().split("\n"))
    # Strip whitespace from header names so keys like "Italian   " become "Italian"
    reader.fieldnames = [name.strip() for name in reader.fieldnames]
    return list(reader)


def ensure_guids(rows: list[dict]) -> int:
    """
    For every row dict, ensure Deck Name, Deck GUID, and Note GUID are populated.
    Modifies rows in-place and returns the number of rows updated.
    """
    updated = 0
    for row in rows:
        italian = row.get("Italian", "").strip()
        category = row.get("Category", "").strip()

        if not italian or not category:
            continue

        deck_name = f"Italian::A1::Vocab::{category}"
        deck_guid = str(stable_id(deck_name))
        note_guid = str(stable_id(italian))

        changed = False
        if row.get("Deck Name", "").strip() != deck_name:
            row["Deck Name"] = deck_name
            changed = True
        if row.get("Deck GUID", "").strip() != deck_guid:
            row["Deck GUID"] = deck_guid
            changed = True
        if not row.get("Note GUID", "").strip():
            row["Note GUID"] = note_guid
            changed = True

        if changed:
            updated += 1

    return updated


def save_vocab_csv(csv_path: str, rows: list[dict], fieldnames: list[str]):
    """Write row dicts back to CSV."""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_decks(rows: list[dict], output_folder: str):
    """
    Group rows by deck name, create one .apkg per deck.
    """
    model = build_vocab_model()

    # Validate all rows up front
    all_errors = []
    for row in rows:
        errors = validate_vocab_row(row)
        all_errors.extend(errors)

    if all_errors:
        print(f"\n=== VALIDATION ERRORS ({len(all_errors)}) ===")
        for err in all_errors:
            print(f"  {err}")
        print()

    # Group by deck name
    deck_groups = {}
    for row in rows:
        deck_name = row.get("Deck Name", "").strip()
        if not deck_name:
            continue
        deck_groups.setdefault(deck_name, []).append(row)

    os.makedirs(output_folder, exist_ok=True)

    created = []
    for deck_name, group in sorted(deck_groups.items()):
        deck_guid = int(group[0]["Deck GUID"].strip())
        deck = genanki.Deck(deck_id=deck_guid, name=deck_name)

        notes_added = 0
        for row in group:
            note_guid = int(row["Note GUID"].strip())
            fields = [
                row.get("Italian", "").strip(),
                row.get("English", "").strip(),
                row.get("Part of Speech", "").strip(),
                row.get("IPA Pronunciation", "").strip(),
                row.get("Gender", "").strip(),
                row.get("Context", "").strip(),
                row.get("Synonyms", "").strip(),
                row.get("Example Sentence", "").strip(),
                row.get("Example Sentence English", "").strip(),
                row.get("Category", "").strip(),
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


def load_config():
    """Load paths from config.json."""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate Anki vocab decks")
    parser.add_argument("--level", default="A1", help="CEFR level (default: A1)")
    parser.add_argument("--source", help="Override source CSV path")
    parser.add_argument("--output", help="Override output folder path")
    args = parser.parse_args()

    config = load_config()
    level_config = config["levels"].get(args.level, {}).get("vocab", {})

    csv_path = args.source or level_config.get("source", "SourceData/A1/Vocab/CardSource/A1_Vocab.csv")
    output_folder = args.output or level_config.get("output", "Decks/A1/Vocab")

    print("Loading CSV...")
    rows = load_vocab_csv(csv_path)
    fieldnames = list(rows[0].keys()) if rows else []

    print("Ensuring GUIDs...")
    updated = ensure_guids(rows)
    print(f"  Updated {updated} rows with deck/note GUIDs.")

    print("Saving CSV...")
    save_vocab_csv(csv_path, rows, fieldnames)

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
