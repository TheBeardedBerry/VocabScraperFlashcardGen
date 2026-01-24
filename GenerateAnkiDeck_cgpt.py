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

def get_italian_verb_model(json_data: dict) -> genanki.Model:
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
        "name": "Infinitive En→It",
        "qfmt": "{{English}}",
        "afmt": "{{FrontSide}}<hr id=\"answer\">" + "<b>Infinitive:</b> {{Infinitive}}" + BACK_COMMON
    })

    templates.append({
        "name": "Infinitive It→En",
        "qfmt": "{{Infinitive}}",
        "afmt": "{{FrontSide}}<hr id=\"answer\">" + "<b>English:</b> {{English}}" + BACK_COMMON
    })

    # Conjugation cards
    for tense, persons in json_data.get("tenses", {}).items():
        for person in persons.keys():
            prefix = f"{tense}_{person}"
            back = (
                f"<div>"
                f"<b>Tense:</b> {tense}<br>"
                f"<b>Conjugation:</b> {{{{{prefix}_conjugation}}}}<br>"
                f"<b>Pronunciation:</b> {{{{{prefix}_pronunciation}}}}<br><br>"
                f"<b>Example (IT):</b> {{{{{prefix}_example}}}}<br>"
                f"<b>Example (EN):</b> {{{{{prefix}_example_english}}}}"
                "</div>"
                + BACK_COMMON
            )

            templates.append({
                "name": f"{tense} {person} En→It",
                "qfmt": f"{{{{{prefix}_english}}}}",
                "afmt": ("{{FrontSide}}<hr id=\"answer\">"
                         f"{{{{{prefix}_conjugation}}}}<br><br>") + back
            })
            templates.append({
                "name": f"{tense} {person} It→En",
                "qfmt": f"{{{{{prefix}_conjugation}}}}",
                "afmt": ("{{FrontSide}}<hr id=\"answer\">"
                         f"{{{{{prefix}_english}}}}<br><br>") + back
            })


    model_name = "Italian Verb Full"
    model_id = stable_id(model_name)
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

    for json_file in files_in_folder:
        if "abitare" in json_file.name:
            json_files.append(json_file)


    return [json.loads(file.read_text(encoding="utf-8")) for file in json_files]


def create_deck_from_folder(json_folder: str, output_apkg: str):
    """
    Load all JSON verb files from `json_folder`, build an Anki deck,
    and write to `output_apkg`.
    """
    verbs = load_json_files(json_folder)
    if not verbs:
        raise ValueError("No JSON verb files found in folder.")

    deck_name = f"Italian Verbs ({len(verbs)})"
    deck_id = stable_id(deck_name)
    deck = genanki.Deck(deck_id, deck_name)

    model = get_italian_verb_model(verbs[0])

    for verb_data in verbs:
        # Build note field values in deterministic order
        fields = [
            verb_data.get("infinitive", ""),
            verb_data.get("infinitive_pronunciation", ""),
            verb_data.get("english", ""),
            str(verb_data.get("regular", "")),
            verb_data.get("context", "")
        ]

        for tense, persons in verb_data.get("tenses", {}).items():
            for person, vals in persons.items():
                prefix = f"{tense}_{person}"
                fields.extend([
                    vals.get("conjugation", ""),
                    vals.get("pronunciation", ""),
                    vals.get("english", ""),
                    vals.get("example", ""),
                    vals.get("example_english", ""),
                ])

        error = False
        # Past participle if present
        pp = verb_data.get("participio_passato", {})
        if pp:
            try:
                fields.extend([
                    pp.get("form", ""),
                    pp.get("pronunciation", ""),
                    pp.get("english", ""),
                    pp.get("example", ""),
                    pp.get("example_english", "")
                ])
            except AttributeError:
                print(f"Error: data missing from verb {verb_data.get("infinitive", "")}")
                continue

        guid = stable_id(verb_data.get("infinitive", ""))
        note = genanki.Note(guid=guid, model=model, fields=fields)
        deck.add_note(note)
        break

    genanki.Package(deck).write_to_file(output_apkg)
    print(f"Deck written to {output_apkg}")


if __name__ == "__main__":
    # Example usage: change these paths as needed
    json_folder = "VerbData/individual_verbs"
    output_apkg = "italian_verbs.apkg"
    create_deck_from_folder(json_folder, output_apkg)