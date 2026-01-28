import os
import json
import genanki
from typing import List
from pathlib import Path
import hashlib

def stable_id(name: str) -> int:
    """
    Generate a stable numeric ID from a string using MD5.
    """
    digest = hashlib.md5(name.encode("utf-8"), usedforsecurity=False).hexdigest()
    # Use first 10 hex digits as an int
    return int(digest[:10], 16)

def get_italian_verb_model(json_data: dict, irregular=False) -> genanki.Model:
    """
    Build a genanki Model for an Italian verb given the JSON data.
    The model includes fields for all parts of the JSON and card templates
    as previously specified (bidirectional cards with full back info).
    """
    # Collect fields from JSON
    fields = [
        {"name": "Infinitive"},
        {"name": "Infinitive_Pronunciation"},
        {"name": "English"},
        {"name": "Regular"},
        {"name": "Context"},
    ]

    # Tense fields
    for tense, persons in json_data.get("tenses", {}).items():
        for person, values in persons.items():
            prefix = f"{tense}_{person}"
            fields.extend([
                {"name": f"{prefix}_conjugation"},
                {"name": f"{prefix}_pronunciation"},
                {"name": f"{prefix}_english"},
                {"name": f"{prefix}_example"},
                {"name": f"{prefix}_example_english"},
            ])

    # Past participle fields if present
    if "participio_passato" in json_data:
        fields.extend([
            {"name": "pp_form"},
            {"name": "pp_pronunciation"},
            {"name": "pp_english"},
            {"name": "pp_example"},
            {"name": "pp_example_english"},
        ])

    # Create templates
    templates = []

    BACK_COMMON = """
    <hr>
    <div>
    <b>Infinitive:</b> {{Infinitive}}<br>
    <b>Context:</b> {{Context}}<br>
    {{#Regular}}
        <b>Regular:</b> Yes<br>
    {{/Regular}}
    {{^Regular}}
        <b style="color:red;font-size:20px">Irregular</b><br>
    {{/Regular}}
    </div>
    """

    # Infinitive cards
    templates.append({
        "name": "Infinitive - En->It",
        "qfmt": "{{English}}",
        "afmt": "{{FrontSide}}<hr id=\"answer\">" + "<b>Infinitive:</b> {{Infinitive}}" + BACK_COMMON
    })

    templates.append({
        "name": "Infinitive - It->En",
        "qfmt": "{{Infinitive}}",
        "afmt": "{{FrontSide}}<hr id=\"answer\">" + "<b>English:</b> {{English}}" + BACK_COMMON
    })

    valid_tenses = ["presente"]


    # Conjugation cards
    for tense, persons in json_data.get("tenses", {}).items():
        if tense not in valid_tenses:
            continue

        for person in persons.keys():
            prefix = f"{tense}_{person}"
            back = (
                f"<div>"
                f"<b>Tense:</b> {tense}<br>"
                f"<b>Pronunciation:</b> {{{{{prefix}_pronunciation}}}}<br><br>"
                f"<b>Example (IT):</b> {{{{{prefix}_example}}}}<br>"
                f"<b>Example (EN):</b> {{{{{prefix}_example_english}}}}"
                "</div>"
                + BACK_COMMON
            )
            print(f"{tense} {person} - En->It")
            templates.append({
                "name": f"{tense} {person} - En->It",
                "qfmt": f"{{{{{prefix}_english}}}}",
                "afmt": ("{{FrontSide}}<hr id=\"answer\">"
                         f"{{{{{prefix}_conjugation}}}}<br><br>") + back
            })
            templates.append({
                "name": f"{tense} {person} - It->En",
                "qfmt": f"{{{{{prefix}_conjugation}}}}",
                "afmt": ("{{FrontSide}}<hr id=\"answer\">"
                         f"{{{{{prefix}_english}}}}<br><br>") + back
            })

    #legacy
    if irregular:
        model_id = stable_id("IrregularVerbModel_Blah")
        model_name = "IrregularVerbs"
    else:
        model_id = stable_id("VerbModel_stuff")
        model_name = "Verbs"

    return genanki.Model(
        model_id,
        model_name,
        fields=fields,
        templates=templates,
        css="""
        .card { font-family: Arial; font-size: 18px; text-align: center; }
        """
    )


def load_json_files(folder: str) -> List[dict]:
    """
    Read all *.json files from the specified folder and return parsed data.
    """
    path = Path(folder)
    json_files = []
    files_in_folder = list(path.glob("*.json"))
    print(f"Found {len(files_in_folder)} files in {folder}")

    for json_file in files_in_folder:
        json_files.append(json_file)


    return [json.loads(file.read_text(encoding="utf-8")) for file in json_files]


def create_decks_from_folder(json_folder: str, output_folder: str = "."):
    """
    Load all JSON verb files from `json_folder`, group by deck_guid,
    and create multiple Anki decks based on the deck_guid in each file.
    """
    verbs = load_json_files(json_folder)
    if not verbs:
        raise ValueError("No JSON verb files found in folder.")

    # Group verbs by deck_guid
    deck_groups = {}
    verbs_without_guid = []

    for verb_data in verbs:
        deck_guid = verb_data.get("deck_guid")
        if deck_guid:
            deck_guid = str(deck_guid)  # Ensure it's a string
            if deck_guid not in deck_groups:
                deck_groups[deck_guid] = []
            deck_groups[deck_guid].append(verb_data)
        else:
            verbs_without_guid.append(verb_data["infinitive"])

    if verbs_without_guid:
        print(f"Warning: {len(verbs_without_guid)} verbs without deck_guid:")
        for verb in verbs_without_guid:
            print(f"  - {verb}")

    print(f"Found {len(deck_groups)} unique deck GUIDs")
    print(f"Total verbs with deck_guid: {sum(len(group) for group in deck_groups.values())}")

    # Create a deck for each deck_guid
    created_decks = []

    for deck_guid, verb_group in deck_groups.items():
        if not verb_group:
            continue

        print(f"\nProcessing deck {deck_guid} with {len(verb_group)} verbs:")

        # Create model based on first verb in group
        model = get_italian_verb_model(verb_group[0])
        irregular_model = get_italian_verb_model(verb_group[0], irregular=True)

        # Get deck name from the JSON data (all verbs in same group should have same deck_name)
        deck_name = verb_group[0].get("deck_name")
        if not deck_name:
            # Fallback to old naming scheme if deck_name is missing
            verb_names = sorted([verb["infinitive"] for verb in verb_group])
            first_verb = verb_names[0]
            last_verb = verb_names[-1]
            deck_name = f"Italian::A1::Verbs::{first_verb}_{last_verb}"
            print(f"    Warning: Using fallback deck name: {deck_name}")

        # Extract first and last verb names for filename (sorted)
        verb_names = sorted([verb["infinitive"] for verb in verb_group])
        first_verb = verb_names[0]
        last_verb = verb_names[-1]

        deck = genanki.Deck(
            deck_id=int(deck_guid),  # Use the actual deck_guid as the deck ID
            name=deck_name
        )

        notes_added = 0

        for verb_data in verb_group:
            print(f"  Processing {verb_data['infinitive']}")

            # Build note field values in deterministic order
            fields = [
                verb_data["infinitive"],
                verb_data["infinitive_pronunciation"],
                verb_data["english"],
                str(verb_data["regular"]),
                verb_data["context"]
            ]

            for tense, persons in verb_data.get("tenses", {}).items():
                for person, vals in persons.items():
                    fields.extend([
                        vals["conjugation"],
                        vals["pronunciation"],
                        vals["english"],
                        vals["example"],
                        vals["example_english"],
                    ])

            # Past participle if present
            pp = verb_data.get("participio_passato", {})
            if pp:
                try:
                    fields.extend([
                        pp["form"],
                        pp["pronunciation"],
                        pp["english"],
                        pp["example"],
                        pp["example_english"]
                    ])
                except (KeyError, TypeError) as e:
                    print(f"    Error: missing participio_passato data for {verb_data['infinitive']}: {e}")
                    continue

            # Validate field count matches model expectations
            expected_field_count = len(model.fields)
            actual_field_count = len(fields)

            if actual_field_count != expected_field_count:
                print(f"    ERROR: Field count mismatch for verb '{verb_data['infinitive']}':")
                print(f"      Expected: {expected_field_count} fields")
                print(f"      Actual: {actual_field_count} fields")
                print(f"      Difference: {actual_field_count - expected_field_count}")
                print(f"      Skipping verb '{verb_data['infinitive']}'")
                continue

            # Get or create note GUID
            note_guid = verb_data.get("note_guid")
            if not note_guid:
                # Generate new GUID and save to JSON file
                note_guid = stable_id(verb_data["infinitive"])
                verb_data["note_guid"] = note_guid

                # Find and update the original JSON file
                verb_infinitive = verb_data["infinitive"]
                json_file_path = None

                # Find the corresponding JSON file
                json_folder_path = Path(json_folder)
                for json_file in json_folder_path.glob("*.json"):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            file_data = json.load(f)
                        if file_data.get("infinitive") == verb_infinitive:
                            json_file_path = json_file
                            break
                    except Exception:
                        continue

                if json_file_path:
                    try:
                        # Update the JSON file with the new note_guid
                        with open(json_file_path, 'w', encoding='utf-8') as f:
                            json.dump(verb_data, f, ensure_ascii=False, indent=2)
                        print(f"    Added note_guid {note_guid} to {verb_infinitive}")
                    except Exception as e:
                        print(f"    Warning: Could not update {json_file_path}: {e}")
                else:
                    print(f"    Warning: Could not find JSON file for {verb_infinitive}")

            if verb_data["regular"]:
                model_to_use = model
            else:
                model_to_use = irregular_model
            note = genanki.Note(guid=note_guid, model=model_to_use, fields=fields)
            deck.add_note(note)
            notes_added += 1

        if notes_added > 0:
            # Write deck to file
            output_filename = f"A1_Verbs_{first_verb}_{last_verb}.apkg"

            genanki.Package(deck).write_to_file(os.path.join(output_folder, output_filename))
            print(f"  Created {output_filename} with {notes_added} verbs")
            print(f"  Deck name: {deck_name}")
            created_decks.append({
                'deck_guid': deck_guid,
                'deck_name': deck_name,
                'filename': output_filename,
                'verb_count': notes_added,
                'first_verb': first_verb,
                'last_verb': last_verb
            })
        else:
            print(f"  Skipping deck {deck_guid} - no valid verbs")

    print(f"\n=== SUMMARY ===")
    print(f"Created {len(created_decks)} deck files:")
    for deck_info in created_decks:
        print(f"  {deck_info['filename']} (GUID: {deck_info['deck_guid']}, {deck_info['verb_count']} verbs)")
        print(f"    Deck name: {deck_info['deck_name']}")

    return created_decks


if __name__ == "__main__":
    # Example usage: change these paths as needed
    json_folder = "VerbData/individual_verbs"
    output_folder = "./Decks"  # Current directory
    create_decks_from_folder(json_folder, output_folder)