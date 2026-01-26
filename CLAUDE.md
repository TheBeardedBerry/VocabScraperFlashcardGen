# CLAUDE.md - VocabScraperFlashcardGen Project Documentation

## Project Overview
This is an Italian vocabulary learning tool that scrapes verb conjugation data and generates flashcard-compatible JSON files for Italian verbs. The project contains comprehensive conjugation data for 99 Italian verbs with pronunciations, examples, and translations.

## Key Directories & Files

### VerbData/individual_verbs/
Contains 99 JSON files, one per Italian verb, with complete conjugation data including:
- **Structure**: Each verb file follows a standardized format with "tenses" wrapper containing presente, futuro_semplice, and passato_prossimo conjugations
- **Content**: IPA pronunciations, English translations, Italian examples with English translations
- **Metadata**: Context explanations, synonyms, auxiliary verb usage, regularity classification

**Example verb file structure (abitare.json)**:
```json
{
  "infinitive": "abitare",
  "infinitive_pronunciation": "/abi'tare/",
  "english": "to live/to dwell",
  "regular": true,
  "auxiliary": "avere",
  "part_of_speech": "verb",
  "context": "Used for place of residence; permanent dwelling vs temporary stays",
  "synonyms": "vivere,risiedere",
  "tenses": {
    "presente": {
      "io": {
        "conjugation": "abito",
        "pronunciation": "/ˈabito/",
        "english": "I live",
        "example": "Abito in una casa grande.",
        "example_english": "I live in a big house."
      }
      // ... other persons
    },
    "futuro_semplice": { /* conjugations */ },
    "passato_prossimo": { /* conjugations */ }
  },
  "participio_passato": {
    "form": "abitato",
    "pronunciation": "/abi'tato/",
    "english": "lived",
    "example": "La casa è stata abitata per molti anni.",
    "example_english": "The house has been lived in for many years."
  }
}
```

### Enhancement System Files

#### verb_enhancements.csv
**Purpose**: Central data source for systematic verb file enhancements
**Usage**: Contains all enhancement data for 99 verbs in structured CSV format
**Columns**:
- `infinitive`: Verb infinitive form
- `infinitive_ipa`: IPA pronunciation of infinitive
- `context`: Usage explanation and clarification
- `synonyms`: Comma-separated modern Italian synonyms
- `reflexive_type`: Classification for reflexive verbs
- `grammar_fixes`: Corrections to apply
- `example_improvements`: Enhanced examples
- `participio_example`: Past participle example

#### update_verb_files.py
**Purpose**: Systematic verb file updater that applies CSV enhancements to JSON files
**Key Functions**:
- `load_enhancements()`: Reads CSV enhancement data
- `update_verb_structure()`: Applies structural changes and enhancements
- `fix_grammar_errors()`: Corrects English translations
- `create_reflexive_english()`: Handles reflexive verb translations

**Usage**: `python update_verb_files.py`

## Important Technical Details

### IPA Pronunciations
- All pronunciations use International Phonetic Alphabet notation
- Format: `/pronunciation/` with stress marks and Italian phonemes
- Applied to infinitives, all conjugations, and past participles

### Verb Classification
- **Regular verbs**: Follow standard -are, -ere, -ire conjugation patterns
- **Irregular verbs**: Have non-standard conjugations (marked as `"regular": false`)
- **Auxiliary usage**: Either "avere" or "essere" for compound tenses

### Reflexive Verbs
- Special handling with proper English reflexive pronouns
- Examples: "myself", "yourself", "himself", "herself", "ourselves", "yourselves", "themselves"
- Detected via reflexive_type classification in CSV

### File Consistency
All 99 verb files have been updated to follow the same structure:
1. Metadata fields (infinitive, pronunciation, english, regular, auxiliary, part_of_speech)
2. Context and synonyms sections
3. "tenses" wrapper containing all conjugations
4. Past participle with example usage

## Common Tasks

### Adding New Verbs
1. Add entry to `verb_enhancements.csv` with all required data
2. Create new JSON file in `VerbData/individual_verbs/`
3. Run `python update_verb_files.py` to apply enhancements
4. Verify JSON structure matches existing files

### Updating Existing Verbs
1. Modify relevant row in `verb_enhancements.csv`
2. Run `python update_verb_files.py`
3. Check specific updated files for accuracy

### Troubleshooting
- **Script errors**: Check for "MANUAL_INPUT_NEEDED" placeholders in JSON files
- **Missing pronunciations**: Ensure IPA format is correct in CSV
- **Structure issues**: Compare problematic files to abitare.json template

### Recently Completed Work
All 99 Italian verb JSON files have been systematically updated with:
- IPA pronunciations for all forms
- Standardized "tenses" structure wrapper
- Context explanations for usage clarification
- Modern Italian synonyms
- Corrected English translations
- Enhanced examples with translations
- Past participle examples

The enhancement system (CSV + Python script) allows for efficient future updates to verb data while maintaining consistency across all files.

## Development Notes
- All verb files were successfully updated except for 3 that contained placeholder content (morire, ottenere, scegliere) which have since been manually completed
- The CSV-driven approach ensures data consistency and makes bulk updates manageable
- Future Claude instances should use the update_verb_files.py script rather than manual file-by-file editing