import csv
import datetime
import hashlib
import unicodedata
from os import path, mkdir, rename
from shutil import copyfile

def stable_id(name: str) -> int:
    """
    Generate a stable numeric ID from a string using MD5.
    Not used for security — only for generating deterministic IDs.
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


def backup_file(file_path):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    directory, file = path.split(file_path)

    extension = file.split('.')[-1]
    basename = file.split('.')[0]

    new_name = f"{basename}.{timestamp}.{extension}"
    new_directory = path.join(directory, 'backup')
    if not path.exists(new_directory):
        mkdir(new_directory)

    new_location = path.join(new_directory, new_name)
    copyfile(file_path, new_location)

def remove_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def add_default_tense(input_dict, tense, pronouns, languages):
    input_dict.setdefault(tense, {})

    for language in languages:
        print(input_dict)
        input_dict[tense].setdefault(language, {})
        for pronoun in pronouns:
            input_dict[tense][language].setdefault(pronoun, "")

    return input_dict