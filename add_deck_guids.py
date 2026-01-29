#!/usr/bin/env python3
"""
Script to add deck_guid entries to verb JSON files based on verb_deck_mapping.csv
"""

import csv
import json
import os
from pathlib import Path


def load_verb_deck_mappings(csv_file_path):
    """
    Load verb to deck GUID mappings from CSV file.

    Args:
        csv_file_path: Path to the verb_deck_mapping.csv file

    Returns:
        dict: Dictionary mapping verb_infinitive to deck_guid
    """
    mappings = {}

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                verb_infinitive = row['verb_infinitive']
                deck_guid = row['deck_guid']
                deck_name = row['deck_name']
                mappings[verb_infinitive] = [deck_guid, deck_name]

        print(f"Loaded {len(mappings)} verb-to-deck mappings from {csv_file_path}")
        return mappings

    except FileNotFoundError:
        print(f"Error: Could not find {csv_file_path}")
        return {}
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
        return {}


def update_verb_json_files(mappings, verb_dir):
    """
    Update JSON files in the verb directory with deck_guid entries.

    Args:
        mappings: Dictionary mapping verb_infinitive to deck_guid
        verb_dir: Path to directory containing individual verb JSON files
    """
    verb_path = Path(verb_dir)

    if not verb_path.exists():
        print(f"Error: Directory {verb_dir} does not exist")
        return

    updated_count = 0
    not_found_count = 0
    error_count = 0

    # Get all JSON files in the directory
    json_files = list(verb_path.glob("*.json"))

    for json_file in json_files:
        try:
            # Load the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                verb_data = json.load(f)

            # Get the verb infinitive from the JSON
            verb_infinitive = verb_data.get('infinitive')

            if not verb_infinitive:
                print(f"Warning: No infinitive found in {json_file.name}")
                error_count += 1
                continue

            # Check if we have a mapping for this verb
            if verb_infinitive in mappings:
                deck_guid, deck_name = mappings[verb_infinitive]

                # Add or update the deck_guid
                verb_data['deck_guid'] = deck_guid
                verb_data['deck_name'] = deck_name

                # Write back to file
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(verb_data, f, ensure_ascii=False, indent=2)

                print(f"Updated {verb_infinitive} with deck_guid {deck_guid}")
                updated_count += 1

            else:
                print(f"Warning: No deck mapping found for verb '{verb_infinitive}'")
                not_found_count += 1

        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
            error_count += 1

    print(f"\nSummary:")
    print(f"  Updated: {updated_count} files")
    print(f"  No mapping found: {not_found_count} files")
    print(f"  Errors: {error_count} files")
    print(f"  Total processed: {len(json_files)} files")


def main():
    """Main function to orchestrate the deck GUID addition process."""
    # File paths
    csv_file_path = "SourceData/A1/Verbs/ProcessData/verb_deck_mapping.csv"
    verb_dir = "SourceData/A1/Verbs"

    print("Adding deck GUIDs to verb JSON files...")
    print(f"CSV file: {csv_file_path}")
    print(f"Verb directory: {verb_dir}")
    print()

    # Load the verb-to-deck mappings
    mappings = load_verb_deck_mappings(csv_file_path)

    if not mappings:
        print("No mappings loaded. Exiting.")
        return

    # Update the verb JSON files
    update_verb_json_files(mappings, verb_dir)

    print("\nDeck GUID addition complete!")


if __name__ == "__main__":
    main()