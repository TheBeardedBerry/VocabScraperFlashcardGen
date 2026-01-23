import datetime, unicodedata
from os import path, mkdir, rename
from shutil import copyfile

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