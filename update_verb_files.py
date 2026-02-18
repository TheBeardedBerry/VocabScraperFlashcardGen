#!/usr/bin/env python3

import json
import csv
import os
import shutil
from datetime import datetime
from typing import Dict, List, Tuple

class VerbFileUpdater:
    def __init__(self, csv_file='verb_enhancements.csv', verb_dir='SourceData/Verbs'):
        self.csv_file = csv_file
        self.verb_dir = verb_dir
        self.enhancements = {}
        self.reflexive_pronouns = {
            'io': 'mi',
            'tu': 'ti',
            'lui': 'si',
            'noi': 'ci',
            'voi': 'vi',
            'loro': 'si'
        }
        self.load_enhancements()

    def load_enhancements(self):
        """Load enhancement data from CSV file"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.enhancements[row['infinitive']] = row
        print(f"Loaded enhancement data for {len(self.enhancements)} verbs")

    def backup_files(self):
        """Create backup of current verb files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"{self.verb_dir}_backup_{timestamp}"
        shutil.copytree(self.verb_dir, backup_dir)
        print(f"Created backup in: {backup_dir}")

    def convert_pronunciation_to_ipa(self, old_pronunciation, infinitive_ipa):
        """Convert simplified phonetic to IPA format based on patterns"""
        if old_pronunciation.startswith('/') and old_pronunciation.endswith('/'):
            return old_pronunciation  # Already in IPA format

        # Simple conversion for conjugated forms based on infinitive IPA
        # This is a simplified approach - more sophisticated logic could be added
        base = infinitive_ipa.strip('/')

        # Apply basic stress and sound conversions
        converted = old_pronunciation.lower()
        converted = converted.replace('ah', 'a')
        converted = converted.replace('ee', 'i')
        converted = converted.replace('eh', 'e')
        converted = converted.replace('oh', 'o')
        converted = converted.replace('oo', 'u')

        # For now, return a basic IPA format
        return f"/{converted}/"

    def fix_grammar_errors(self, text, grammar_fixes):
        """Apply specific grammar error fixes"""
        if not grammar_fixes:
            return text

        fixes = grammar_fixes.split(',')
        for fix in fixes:
            if '→' in fix:
                old, new = fix.split('→')
                text = text.replace(old.strip(), new.strip())
        return text

    def create_reflexive_english(self, base_english, pronoun):
        """Convert regular English to reflexive form where appropriate"""
        reflexive_mappings = {
            'io': 'myself',
            'tu': 'yourself',
            'lui': 'himself/herself',
            'noi': 'ourselves',
            'voi': 'yourselves',
            'loro': 'themselves'
        }

        # Some verbs don't need explicit reflexive in English
        non_explicit_reflexive = ['apologize', 'have fun', 'worry', 'wake up']

        for verb in non_explicit_reflexive:
            if verb in base_english.lower():
                return base_english

        # Add reflexive pronoun for appropriate verbs
        if any(word in base_english.lower() for word in ['get up', 'sit down', 'get']):
            pronoun_word = reflexive_mappings.get(pronoun, 'oneself')
            return f"{base_english.replace('get up', 'get ' + pronoun_word + ' up').replace('sit down', 'sit ' + pronoun_word + ' down')}"

        return base_english

    def improve_examples(self, verb_data, enhancement_type, infinitive):
        """Improve example sentences based on enhancement type"""
        if enhancement_type == 'contextual':
            # Examples are already good in the current structure
            pass
        elif enhancement_type == 'reflexive_contextual':
            # Handle reflexive examples - already properly structured
            pass
        # More enhancement types can be added here

    def update_verb_structure(self, verb_data, enhancements):
        """Apply all structural updates to a verb"""
        infinitive = enhancements['infinitive']

        # Add new metadata fields
        verb_data['part_of_speech'] = 'verb'
        verb_data['context'] = enhancements['context']
        verb_data['synonyms'] = enhancements['synonyms']

        # Update infinitive pronunciation to IPA
        verb_data['infinitive_pronunciation'] = enhancements['infinitive_ipa']

        # Wrap tenses if not already wrapped
        if 'tenses' not in verb_data:
            tenses = {}
            for tense_name in ['presente', 'futuro_simplice', 'passato_prossimo']:
                if tense_name in verb_data:
                    tenses[tense_name] = verb_data.pop(tense_name)
            if tenses:
                verb_data['tenses'] = tenses

        # Update pronunciations in all conjugated forms
        if 'tenses' in verb_data:
            for tense_name, tense_data in verb_data['tenses'].items():
                if isinstance(tense_data, dict):
                    for pronoun, pronoun_data in tense_data.items():
                        if isinstance(pronoun_data, dict) and 'pronunciation' in pronoun_data:
                            old_pronunciation = pronoun_data['pronunciation']
                            new_pronunciation = self.convert_pronunciation_to_ipa(
                                old_pronunciation, enhancements['infinitive_ipa']
                            )
                            pronoun_data['pronunciation'] = new_pronunciation

                            # Fix grammar errors in English translations
                            if 'english' in pronoun_data:
                                pronoun_data['english'] = self.fix_grammar_errors(
                                    pronoun_data['english'], enhancements.get('grammar_fixes', '')
                                )

                            # Fix grammar errors in examples
                            if 'example_english' in pronoun_data:
                                pronoun_data['example_english'] = self.fix_grammar_errors(
                                    pronoun_data['example_english'], enhancements.get('grammar_fixes', '')
                                )

                            # Handle reflexive translations
                            if enhancements['reflexive_type'] == 'reflexive' and 'english' in pronoun_data:
                                pronoun_data['english'] = self.create_reflexive_english(
                                    pronoun_data['english'], pronoun
                                )

        # Update participio_passato
        if 'participio_passato' in verb_data:
            # Fix pronunciation
            if 'pronunciation' in verb_data['participio_passato']:
                old_pronunciation = verb_data['participio_passato']['pronunciation']
                verb_data['participio_passato']['pronunciation'] = self.convert_pronunciation_to_ipa(
                    old_pronunciation, enhancements['infinitive_ipa']
                )

            # Fix grammar in English
            if 'english' in verb_data['participio_passato']:
                verb_data['participio_passato']['english'] = self.fix_grammar_errors(
                    verb_data['participio_passato']['english'], enhancements.get('grammar_fixes', '')
                )

            # Add example if missing
            if 'example' not in verb_data['participio_passato']:
                verb_data['participio_passato']['example'] = enhancements['participio_example']
                verb_data['participio_passato']['example_english'] = self.translate_participio_example(
                    enhancements['participio_example']
                )

        return verb_data

    def translate_participio_example(self, italian_example):
        """Basic translation for participio examples - can be enhanced"""
        # This is a simplified translation - in a real implementation,
        # you might want to include actual translations in the CSV
        translations = {
            "È stato un grande onore conoscerti.": "It was a great honor to meet you.",
            "La casa è stata abitata per molti anni.": "The house has been lived in for many years.",
            "La persona aiutata ha mostrato grande gratitudine.": "The helped person showed great gratitude.",
            "Il bambino è stato alzato dalla mamma per andare a scuola.": "The child was woken up by his mother to go to school.",
        }

        return translations.get(italian_example, "Example in English")

    def update_single_verb(self, infinitive):
        """Update a single verb file"""
        file_path = os.path.join(self.verb_dir, f"{infinitive}.json")

        if not os.path.exists(file_path):
            print(f"Warning: File not found for {infinitive}")
            return False

        if infinitive not in self.enhancements:
            print(f"Warning: No enhancement data for {infinitive}")
            return False

        try:
            # Load current verb data
            with open(file_path, 'r', encoding='utf-8') as f:
                verb_data = json.load(f)

            # Apply enhancements
            updated_data = self.update_verb_structure(verb_data, self.enhancements[infinitive])

            # Save updated data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)

            print(f"✓ Updated {infinitive}.json")
            return True

        except Exception as e:
            print(f"✗ Error updating {infinitive}: {e}")
            return False

    def update_all_verbs(self):
        """Update all verb files"""
        print("Starting systematic update of all verb files...")

        # Create backup first
        self.backup_files()

        success_count = 0
        total_count = len(self.enhancements)

        for infinitive in self.enhancements.keys():
            if self.update_single_verb(infinitive):
                success_count += 1

        print(f"\nUpdate complete: {success_count}/{total_count} files updated successfully")

        if success_count == total_count:
            print("🎉 All verb files updated successfully!")
        else:
            print(f"⚠️  {total_count - success_count} files had issues")

    def validate_updates(self):
        """Validate that all updates were applied correctly"""
        print("Validating updates...")

        issues = []

        for infinitive in self.enhancements.keys():
            file_path = os.path.join(self.verb_dir, f"{infinitive}.json")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    verb_data = json.load(f)

                # Check required fields
                required_fields = ['part_of_speech', 'context', 'synonyms', 'tenses']
                for field in required_fields:
                    if field not in verb_data:
                        issues.append(f"{infinitive}: Missing {field}")

                # Check IPA format
                if not verb_data.get('infinitive_pronunciation', '').startswith('/'):
                    issues.append(f"{infinitive}: Infinitive pronunciation not in IPA format")

            except Exception as e:
                issues.append(f"{infinitive}: Error reading file - {e}")

        if not issues:
            print("✓ All validations passed!")
        else:
            print(f"⚠️  Found {len(issues)} validation issues:")
            for issue in issues[:10]:  # Show first 10 issues
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")

def main():
    """Main execution function"""
    print("Italian Verb File Updater")
    print("=" * 40)

    updater = VerbFileUpdater()

    # Update all verb files
    updater.update_all_verbs()

    # Validate updates
    updater.validate_updates()

    print("\nProcess complete!")

if __name__ == "__main__":
    main()