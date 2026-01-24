#!/usr/bin/env python3

import json
from json_generator import VerbJSONGenerator

def generate_all_regular_verbs():
    """Generate JSON files for all regular verbs"""
    generator = VerbJSONGenerator()

    # Get all regular verb categories
    regular_categories = [
        'regular_are',
        'regular_ere',
        'regular_ire_type1',
        'regular_ire_type2',
        'reflexive'
    ]

    total_generated = 0

    for category in regular_categories:
        verbs = generator.categories['classification'][category]
        print(f"\nGenerating {category} verbs ({len(verbs)} verbs):")

        for verb in verbs:
            try:
                generator.save_verb_json(verb)
                total_generated += 1
            except Exception as e:
                print(f"Error generating {verb}: {e}")

    print(f"\nTotal regular verbs generated: {total_generated}")

    # Show irregular verbs that need manual handling
    irregular_verbs = generator.categories['classification']['irregular']
    print(f"\nIrregular verbs needing manual input ({len(irregular_verbs)} verbs):")
    for verb in irregular_verbs:
        print(f"  - {verb}")

def create_irregular_templates():
    """Create template files for irregular verbs"""
    generator = VerbJSONGenerator()
    irregular_verbs = generator.categories['classification']['irregular']

    # Template for irregular verbs
    irregular_template = {
        "infinitive": "",
        "infinitive_pronunciation": "MANUAL_INPUT_NEEDED",
        "english": "",
        "regular": False,
        "auxiliary": "",
        "present_tense": {
            "io": {
                "conjugation": "MANUAL_INPUT_NEEDED",
                "pronunciation": "MANUAL_INPUT_NEEDED",
                "english": "MANUAL_INPUT_NEEDED",
                "example": "MANUAL_INPUT_NEEDED",
                "example_english": "MANUAL_INPUT_NEEDED"
            },
            "tu": "MANUAL_INPUT_NEEDED",
            "lui_lei": "MANUAL_INPUT_NEEDED",
            "noi": "MANUAL_INPUT_NEEDED",
            "voi": "MANUAL_INPUT_NEEDED",
            "loro": "MANUAL_INPUT_NEEDED"
        },
        "past_tense": "MANUAL_INPUT_NEEDED",
        "future_tense": "MANUAL_INPUT_NEEDED",
        "past_participle": "MANUAL_INPUT_NEEDED"
    }

    print(f"Creating templates for {len(irregular_verbs)} irregular verbs...")

    for verb in irregular_verbs:
        template = irregular_template.copy()
        template["infinitive"] = verb
        template["english"] = generator.verb_translations.get(verb, f"to {verb}")
        template["auxiliary"] = generator.get_auxiliary(verb)

        filename = f"VerbData/individual_verbs/{verb}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        print(f"Created template: {filename}")

if __name__ == "__main__":
    print("=== Generating All Regular Verbs ===")
    generate_all_regular_verbs()

    print("\n=== Creating Irregular Verb Templates ===")
    create_irregular_templates()

    print("\n=== Summary ===")
    print("✅ Regular verbs: Generated with full conjugations")
    print("⚠️  Irregular verbs: Templates created - need manual completion")
    print("\nNext steps:")
    print("1. Review generated regular verb files")
    print("2. Complete irregular verb templates manually")
    print("3. Validate all files")
    print("4. Create combined JSON file")