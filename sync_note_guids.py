# Copyright © 2026 Christopher C Berry All Rights Reserved.
# _______________________________________________
# sync_note_guids.py
# Reads A1_Vocab_backup.csv, calculates stable_id from italian+english,
# and populates the note_guid column in A1_Vocab.csv for matching words.

import csv
import hashlib


def stable_id(name: str) -> int:
    """
    Generate a stable numeric ID from a string using MD5.
    """
    digest = hashlib.md5(name.encode("utf-8"), usedforsecurity=False).hexdigest()
    return int(digest[:10], 16)


def load_csv(csv_path: str):
    """Read the CSV and return (header, rows). Rows are lists of strings."""
    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n").replace("\r", "\n")
    reader = csv.reader(content.strip().split("\n"))
    all_rows = list(reader)
    header = all_rows[0]
    data_rows = all_rows[1:]
    return header, data_rows


def save_csv(csv_path: str, header, rows):
    """Write header + rows back to the CSV."""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    backup_path = "A1_Vocab_backup.csv"
    main_path = "A1_Vocab.csv"

    # Column indices
    COL_ITALIAN = 0
    COL_ENGLISH = 1
    COL_NOTE_GUID = 12

    print(f"Loading {backup_path}...")
    backup_header, backup_rows = load_csv(backup_path)

    # Build a lookup: italian -> note_guid (calculated from italian+english)
    guid_lookup = {}
    for row in backup_rows:
        if len(row) < 2:
            continue
        italian = row[COL_ITALIAN].strip()
        english = row[COL_ENGLISH].strip()
        if italian and english:
            note_guid = str(stable_id(f"{italian}{english}"))
            guid_lookup[italian] = note_guid

    print(f"  Found {len(guid_lookup)} words in backup")

    print(f"Loading {main_path}...")
    main_header, main_rows = load_csv(main_path)

    updated = 0
    for row in main_rows:
        # Ensure row has enough columns
        while len(row) < 13:
            row.append("")

        italian = row[COL_ITALIAN].strip()
        if italian in guid_lookup:
            new_guid = guid_lookup[italian]
            if row[COL_NOTE_GUID].strip() != new_guid:
                row[COL_NOTE_GUID] = new_guid
                updated += 1

    print(f"  Updated {updated} note GUIDs")

    print(f"Saving {main_path}...")
    save_csv(main_path, main_header, main_rows)

    print("Done.")


if __name__ == "__main__":
    main()
