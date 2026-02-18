# Copyright (C) 2026 Christopher C Berry All Rights Reserved.
# _______________________________________________
# GenerateAnkiDeck_cgpt.py
# Reads verb JSON files, validates them, ensures stable GUIDs,
# and generates Anki .apkg decks grouped by deck_guid.

import argparse
import json
import os
from pathlib import Path
from typing import List

import genanki

from helpers import stable_id
from schemas import (
    ACTIVE_TENSES,
    CONJUGATION_FIELDS,
    IRREGULAR_VERB_MODEL_SEED,
    PP_FIELDS,
    VERB_METADATA_FIELDS,
    VERB_MODEL_SEED,
    VERB_PERSONS,
    VERB_TENSES,
    build_verb_field_names,
    validate_verb_data,
)

TEMPLATE_DIR = Path(__file__).parent / "templates" / "verb"


def _read_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def get_italian_verb_model(irregular=False) -> genanki.Model:
    """
    Build a genanki Model for Italian verbs using the canonical field schema.
    The field list is deterministic and independent of any single verb file.
    """
    fields = [{"name": n} for n in build_verb_field_names()]

    back_common = _read_template("back_common.html")
    css = _read_template("card.css")

    templates = []

    # Infinitive cards
    templates.append({
        "name": "Infinitive - En->It",
        "qfmt": _read_template("infinitive_en_it.html"),
        "afmt": _read_template("infinitive_en_it_back.html") + back_common,
    })
    templates.append({
        "name": "Infinitive - It->En",
        "qfmt": _read_template("infinitive_it_en.html"),
        "afmt": _read_template("infinitive_it_en_back.html") + back_common,
    })

    # Conjugation cards — only for active tenses
    conj_en_it_front = _read_template("conjugation_en_it.html")
    conj_en_it_back = _read_template("conjugation_en_it_back.html")
    conj_it_en_front = _read_template("conjugation_it_en.html")
    conj_it_en_back = _read_template("conjugation_it_en_back.html")

    for tense in VERB_TENSES:
        if tense not in ACTIVE_TENSES:
            continue
        for person in VERB_PERSONS:
            prefix = f"{tense}_{person}"
            # Replace PREFIX and TENSE_NAME placeholders in templates
            en_it_q = conj_en_it_front.replace("PREFIX", prefix)
            en_it_a = (conj_en_it_back.replace("PREFIX", prefix)
                       .replace("TENSE_NAME", tense) + back_common)
            it_en_q = conj_it_en_front.replace("PREFIX", prefix)
            it_en_a = (conj_it_en_back.replace("PREFIX", prefix)
                       .replace("TENSE_NAME", tense) + back_common)

            templates.append({
                "name": f"{tense} {person} - En->It",
                "qfmt": en_it_q,
                "afmt": en_it_a,
            })
            templates.append({
                "name": f"{tense} {person} - It->En",
                "qfmt": it_en_q,
                "afmt": it_en_a,
            })

    # WARNING: changing these seeds will break existing Anki decks.
    if not irregular:
        model_id = stable_id(VERB_MODEL_SEED)
        model_name = "Verbs"
    else:
        model_id = stable_id(IRREGULAR_VERB_MODEL_SEED)
        model_name = "IrregularVerbs"

    return genanki.Model(
        model_id,
        model_name,
        fields=fields,
        templates=templates,
        css=css,
    )


def load_json_files(folder: str) -> List[dict]:
    """Read all *.json files from the specified folder and return parsed data."""
    path = Path(folder)
    files = list(path.glob("*.json"))
    print(f"Found {len(files)} files in {folder}")
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]


def ensure_verb_guids(json_folder: str):
    """
    Assign note_guid to any verb JSON files that lack one.
    This is a separate preparatory step that runs before generation,
    keeping generation itself read-only.
    """
    folder = Path(json_folder)
    updated = 0
    for json_file in folder.glob("*.json"):
        data = json.loads(json_file.read_text(encoding="utf-8"))
        if not data.get("note_guid"):
            data["note_guid"] = stable_id(data["infinitive"])
            json_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"  Added note_guid to {data['infinitive']}")
            updated += 1
    if updated:
        print(f"  Assigned {updated} new note GUIDs")
    return updated


def extract_fields(verb_data: dict) -> list[str]:
    """
    Extract field values from verb JSON in canonical order.
    Uses the explicit schema rather than iterating over the verb's own keys.
    """
    fields = [
        verb_data["infinitive"],
        verb_data["infinitive_pronunciation"],
        verb_data["english"],
        str(verb_data["regular"]),
        verb_data["context"],
    ]

    tenses = verb_data.get("tenses", {})
    for tense in VERB_TENSES:
        persons = tenses.get(tense, {})
        for person in VERB_PERSONS:
            vals = persons.get(person, {})
            for key in CONJUGATION_FIELDS:
                fields.append(vals.get(key, ""))

    pp = verb_data.get("participio_passato", {})
    fields.extend([
        pp.get("form", ""),
        pp.get("pronunciation", ""),
        pp.get("english", ""),
        pp.get("example", ""),
        pp.get("example_english", ""),
    ])

    return fields


def create_decks_from_folder(json_folder: str, output_folder: str = "."):
    """
    Load all JSON verb files, validate, group by deck_guid,
    and create Anki decks.
    """
    # Step 1: Ensure all verbs have GUIDs (separate from generation)
    ensure_verb_guids(json_folder)

    # Step 2: Load and validate
    verbs = load_json_files(json_folder)
    if not verbs:
        raise ValueError("No JSON verb files found in folder.")

    all_errors = []
    for verb_data in verbs:
        errors = validate_verb_data(verb_data)
        all_errors.extend(errors)

    if all_errors:
        print(f"\n=== VALIDATION ERRORS ({len(all_errors)}) ===")
        for err in all_errors:
            print(f"  {err}")
        print()

    # Step 3: Build models (deterministic, not data-dependent)
    model = get_italian_verb_model(irregular=False)
    irregular_model = get_italian_verb_model(irregular=True)
    expected_field_count = len(model.fields)

    # Step 4: Group by deck_guid
    deck_groups = {}
    verbs_without_guid = []

    for verb_data in verbs:
        deck_guid = verb_data.get("deck_guid")
        if deck_guid:
            deck_guid = str(deck_guid)
            deck_groups.setdefault(deck_guid, []).append(verb_data)
        else:
            verbs_without_guid.append(verb_data["infinitive"])

    if verbs_without_guid:
        print(f"Warning: {len(verbs_without_guid)} verbs without deck_guid:")
        for verb in verbs_without_guid:
            print(f"  - {verb}")

    print(f"Found {len(deck_groups)} unique deck GUIDs")
    print(f"Total verbs with deck_guid: {sum(len(g) for g in deck_groups.values())}")

    # Step 5: Create decks
    os.makedirs(output_folder, exist_ok=True)
    created_decks = []

    for deck_guid, verb_group in deck_groups.items():
        if not verb_group:
            continue

        print(f"\nProcessing deck {deck_guid} with {len(verb_group)} verbs:")

        deck_name = verb_group[0].get("deck_name")
        if not deck_name:
            verb_names = sorted([v["infinitive"] for v in verb_group])
            deck_name = f"Italian::A1::Verbs::{verb_names[0]}_{verb_names[-1]}"
            print(f"    Warning: Using fallback deck name: {deck_name}")

        verb_names = sorted([v["infinitive"] for v in verb_group])
        first_verb = verb_names[0]
        last_verb = verb_names[-1]

        deck = genanki.Deck(deck_id=int(deck_guid), name=deck_name)
        notes_added = 0

        for verb_data in verb_group:
            print(f"  Processing {verb_data['infinitive']}")

            fields = extract_fields(verb_data)

            if len(fields) != expected_field_count:
                print(f"    ERROR: Field count mismatch for '{verb_data['infinitive']}':")
                print(f"      Expected: {expected_field_count}, Actual: {len(fields)}")
                print(f"      Skipping verb '{verb_data['infinitive']}'")
                continue

            note_guid = verb_data.get("note_guid")
            model_to_use = model if verb_data["regular"] else irregular_model

            note = genanki.Note(guid=note_guid, model=model_to_use, fields=fields)
            deck.add_note(note)
            notes_added += 1

        if notes_added > 0:
            output_filename = f"A1_Verbs_{first_verb}_{last_verb}.apkg"
            genanki.Package(deck).write_to_file(
                os.path.join(output_folder, output_filename)
            )
            print(f"  Created {output_filename} with {notes_added} verbs")
            print(f"  Deck name: {deck_name}")
            created_decks.append({
                "deck_guid": deck_guid,
                "deck_name": deck_name,
                "filename": output_filename,
                "verb_count": notes_added,
                "first_verb": first_verb,
                "last_verb": last_verb,
            })
        else:
            print(f"  Skipping deck {deck_guid} - no valid verbs")

    print(f"\n=== SUMMARY ===")
    print(f"Created {len(created_decks)} deck files:")
    for info in created_decks:
        print(f"  {info['filename']} (GUID: {info['deck_guid']}, {info['verb_count']} verbs)")
        print(f"    Deck name: {info['deck_name']}")

    return created_decks


def load_config():
    """Load paths from config.json."""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Anki verb decks")
    parser.add_argument("--level", default="A1", help="CEFR level (default: A1)")
    parser.add_argument("--source", help="Override source folder path")
    parser.add_argument("--output", help="Override output folder path")
    args = parser.parse_args()

    config = load_config()
    level_config = config["levels"].get(args.level, {}).get("verbs", {})

    json_folder = args.source or level_config.get("source", "SourceData/A1/Verbs/CardSource")
    output_folder = args.output or level_config.get("output", "Decks/A1/Verbs")

    create_decks_from_folder(json_folder, output_folder)
