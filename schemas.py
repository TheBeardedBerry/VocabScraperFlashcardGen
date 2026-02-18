# schemas.py
# Canonical schema definitions for verb and vocab card types.
# These define the expected structure of source data and the deterministic
# field ordering used by Anki models.

# WARNING: changing these model seed strings will break existing Anki decks.
# They are locked to the values originally used for deck generation.
VERB_MODEL_SEED = "VerbModel_stuff"
IRREGULAR_VERB_MODEL_SEED = "IrregularVerbModel_Blah"
VOCAB_MODEL_SEED = "Words"

# Canonical tense ordering — all verb JSON files must contain these tenses.
# Note: "futuro_simplice" is a historical misspelling that is preserved for
# compatibility with existing data files.
VERB_TENSES = ["presente", "futuro_simplice", "passato_prossimo"]

# Canonical person ordering within each tense.
VERB_PERSONS = ["io", "tu", "lui", "noi", "voi", "loro"]

# Per-person fields inside each tense block.
CONJUGATION_FIELDS = ["conjugation", "pronunciation", "english", "example", "example_english"]

# Top-level metadata fields (in order) that appear before tense data.
VERB_METADATA_FIELDS = [
    "Infinitive",
    "Infinitive_Pronunciation",
    "English",
    "Regular",
    "Context",
]

# Past participle fields (appended after all tense fields).
PP_FIELDS = ["pp_form", "pp_pronunciation", "pp_english", "pp_example", "pp_example_english"]

# Tenses for which card templates are generated.
# Extend this list to enable cards for additional tenses.
ACTIVE_TENSES = ["presente"]

# Vocab CSV expected column names (used with csv.DictReader).
VOCAB_COLUMNS = [
    "Italian",
    "English",
    "Part of Speech",
    "IPA Pronunciation",
    "Gender",
    "Context",
    "Synonyms",
    "Example Sentence",
    "Example Sentence English",
    "Category",
    "Deck Name",
    "Deck GUID",
    "Note GUID",
]

# Fields included in the Anki vocab model (subset of VOCAB_COLUMNS, no GUID/deck cols).
VOCAB_MODEL_FIELDS = [
    "Italian",
    "English",
    "PartOfSpeech",
    "IPA",
    "Gender",
    "Context",
    "Synonyms",
    "ExampleIT",
    "ExampleEN",
    "Category",
]


def build_verb_field_names():
    """Return the canonical ordered list of Anki field names for verb cards."""
    fields = list(VERB_METADATA_FIELDS)
    for tense in VERB_TENSES:
        for person in VERB_PERSONS:
            prefix = f"{tense}_{person}"
            for suffix in CONJUGATION_FIELDS:
                fields.append(f"{prefix}_{suffix}")
    fields.extend(PP_FIELDS)
    return fields


def validate_verb_data(verb_data: dict) -> list[str]:
    """
    Validate a verb JSON dict against the canonical schema.
    Returns a list of error strings (empty if valid).
    """
    errors = []
    infinitive = verb_data.get("infinitive", "<unknown>")

    for key in ("infinitive", "infinitive_pronunciation", "english", "regular", "context"):
        if key not in verb_data:
            errors.append(f"{infinitive}: missing top-level field '{key}'")

    tenses = verb_data.get("tenses", {})
    for tense in VERB_TENSES:
        if tense not in tenses:
            errors.append(f"{infinitive}: missing tense '{tense}'")
            continue
        for person in VERB_PERSONS:
            if person not in tenses[tense]:
                errors.append(f"{infinitive}: missing person '{person}' in tense '{tense}'")
                continue
            for field in CONJUGATION_FIELDS:
                if field not in tenses[tense][person]:
                    errors.append(f"{infinitive}: missing field '{field}' in {tense}.{person}")

    pp = verb_data.get("participio_passato")
    if not pp:
        errors.append(f"{infinitive}: missing 'participio_passato'")
    else:
        for field in ("form", "pronunciation", "english", "example", "example_english"):
            if field not in pp:
                errors.append(f"{infinitive}: missing '{field}' in participio_passato")

    return errors


def validate_vocab_row(row: dict) -> list[str]:
    """
    Validate a vocab CSV row (as a dict from DictReader) against expected columns.
    Returns a list of error strings (empty if valid).
    """
    errors = []
    italian = row.get("Italian", "<unknown>").strip()

    for col in ("Italian", "English", "Category"):
        val = row.get(col, "").strip()
        if not val:
            errors.append(f"'{italian}': missing required column '{col}'")

    return errors
