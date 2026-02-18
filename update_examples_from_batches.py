#!/usr/bin/env python3
"""
Enhanced Example Updater for Italian Verb JSON files

This script processes multiple CSV batch files containing improved example sentences
and updates the corresponding verb JSON files with longer, more detailed examples.

CSV Format expected:
infinitive,tense,person,new_example,new_example_english

Usage: python update_examples_from_batches.py
"""

import json
import csv
import os
import glob
from pathlib import Path


class ExampleUpdater:
    def __init__(self, verb_dir='SourceData/Verbs'):
        self.verb_dir = Path(verb_dir)
        self.batch_files = []
        self.updates_applied = 0
        self.files_updated = 0

        # Find all batch CSV files
        self.find_batch_files()

    def find_batch_files(self):
        """Find all example improvement batch CSV files"""
        pattern = "example_improvements_batch*.csv"
        self.batch_files = sorted(glob.glob(pattern))
        print(f"Found {len(self.batch_files)} batch files: {self.batch_files}")

    def load_all_batch_data(self):
        """Load example improvements from all batch CSV files"""
        all_examples = {}

        for batch_file in self.batch_files:
            print(f"Loading {batch_file}...")
            try:
                with open(batch_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    batch_count = 0

                    for row in reader:
                        infinitive = row['infinitive'].strip()
                        tense = row['tense'].strip()
                        person = row['person'].strip()
                        new_example = row['new_example'].strip()
                        new_example_english = row['new_example_english'].strip()

                        if infinitive not in all_examples:
                            all_examples[infinitive] = {}
                        if tense not in all_examples[infinitive]:
                            all_examples[infinitive][tense] = {}

                        all_examples[infinitive][tense][person] = {
                            'example': new_example,
                            'example_english': new_example_english
                        }
                        batch_count += 1

                    print(f"  Loaded {batch_count} example updates from {batch_file}")

            except Exception as e:
                print(f"Error loading {batch_file}: {e}")
                continue

        total_verbs = len(all_examples)
        total_updates = sum(
            len(tenses) * len(persons)
            for tenses in all_examples.values()
            for persons in tenses.values()
        )
        print(f"Total: {total_updates} example updates for {total_verbs} verbs")
        return all_examples

    def update_verb_file(self, infinitive, example_data):
        """Update a single verb JSON file with new examples"""
        file_path = self.verb_dir / f"{infinitive}.json"

        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            return False

        try:
            # Load existing verb data
            with open(file_path, 'r', encoding='utf-8') as file:
                verb_data = json.load(file)

            # Track updates for this file
            file_updates = 0

            # Update examples in tenses
            if 'tenses' in verb_data:
                for tense_name, tense_data in verb_data['tenses'].items():
                    if tense_name in example_data:
                        for person, person_data in tense_data.items():
                            if person in example_data[tense_name]:
                                if isinstance(person_data, dict):
                                    # Update the example sentences
                                    old_example = person_data.get('example', '')
                                    old_example_english = person_data.get('example_english', '')

                                    person_data['example'] = example_data[tense_name][person]['example']
                                    person_data['example_english'] = example_data[tense_name][person]['example_english']

                                    file_updates += 1
                                    self.updates_applied += 1

                                    # Show what changed (truncated for readability)
                                    old_short = (old_example[:50] + "...") if len(old_example) > 50 else old_example
                                    new_short = (person_data['example'][:50] + "...") if len(person_data['example']) > 50 else person_data['example']
                                    print(f"    {tense_name}.{person}: '{old_short}' → '{new_short}'")

            if file_updates > 0:
                # Save updated verb data
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(verb_data, file, ensure_ascii=False, indent=2)

                print(f"✅ Updated {infinitive}.json ({file_updates} examples)")
                self.files_updated += 1
                return True
            else:
                print(f"ℹ️  No updates needed for {infinitive}.json")
                return False

        except Exception as e:
            print(f"❌ Error updating {infinitive}.json: {e}")
            return False

    def process_all_updates(self):
        """Process all example updates from batch files"""
        print("=" * 60)
        print("ENHANCED EXAMPLE UPDATER")
        print("=" * 60)

        # Load all batch data
        all_examples = self.load_all_batch_data()

        if not all_examples:
            print("❌ No example data loaded from batch files")
            return

        print(f"\n📝 Processing example updates...")
        print("-" * 40)

        # Update each verb file
        for infinitive, example_data in all_examples.items():
            print(f"\n🔄 Updating {infinitive}...")
            self.update_verb_file(infinitive, example_data)

        # Summary
        print("\n" + "=" * 60)
        print("UPDATE SUMMARY")
        print("=" * 60)
        print(f"✅ Files updated: {self.files_updated}")
        print(f"🔄 Total example updates applied: {self.updates_applied}")
        print(f"📁 Batch files processed: {len(self.batch_files)}")

        if self.files_updated > 0:
            print(f"\n🎉 Successfully enhanced examples for {self.files_updated} verb files!")
        else:
            print(f"\n⚠️  No files were updated. Check batch file format and verb file availability.")


def main():
    """Main execution function"""
    updater = ExampleUpdater()
    updater.process_all_updates()


if __name__ == "__main__":
    main()