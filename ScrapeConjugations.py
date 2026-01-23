#!/usr/bin/env python3

#packages to install:
# pip install soupsieve
# pip install beautifulsoup4
# pip install bs4
# pip install dnspython
# pip install pymongo

import requests  # lib to make web requests
import json
from bs4 import BeautifulSoup
import helpers, shutil
from os import rename, path
from verb_scraper import VerbScraper

output_json = 'VocabData/verb_data.json'
temp_output_json = 'VocabData/temp_verb_data.json'
output_file = 'VocabData/verb_output.csv'
temp_output_file = 'VocabData/temp_verb_output.csv'

verb_template = {
  "locked": False, # this tells the program to skip this because the term had to be written by hand.
  "override": {}
}

pronoun_translations = {
  "io": "I",
  "tu": "You",
  "lui": "He/She/It",
  "noi": "We",
  "voi": "You all",
  "loro": "They"
}

languages = [
  "en",
  "it"
]
def scrape_conjugations(OnlyMissing=False):

  scraper = VerbScraper()

  verb_data = {}
  if path.exists(output_json):
    with open(output_json) as existing_verb_data:
      verb_data = json.load(existing_verb_data)

  try:
    with (open('A1_Verbs.txt') as verb_list_file):
      verb_list = []
      verb_list = [line.rstrip() for line in verb_list_file]

      # create empty data list
      data = []

    with open('patterns/verb_exceptions.json') as verb_exceptions_file:
      verb_exceptions = json.load(verb_exceptions_file)

    # loop through vocab input
    for verb in verb_list:

      if verb in verb_data.keys():
        current_verb_data = verb_data[verb]
      else:
        current_verb_data = verb_template

      # run through all of the tense, pronoun combinations and either populate a list with everything OR only the missing items.
      missing_data = []
      for tense in scraper.tenses:
        for pronoun in scraper.pronouns:
          if OnlyMissing and current_verb_data:
            try:
              it = current_verb_data[tense]["it"][pronoun]
              en = current_verb_data[tense]["en"][pronoun]
            except KeyError:
              missing_data.append([tense, pronoun])
          else:
            missing_data.append([tense, pronoun])

      #add infinitive translation in if its missing
      if not "en" in current_verb_data:
        missing_data.append(["infinitive", ""])

      #try:
      for data in missing_data:
        tense, pronoun = data

        current_verb_data = helpers.add_default_tense(current_verb_data, tense, scraper.pronouns, languages)

        if tense == "infinitive":
          current_verb_data["infinitive"] = scraper.get_conjugation(verb, tense, pronoun, "en")
          continue

        it_conj = scraper.get_conjugation(verb, tense, pronoun, "it")

        if tense in current_verb_data["override"].keys():
          eng_override = current_verb_data["override"][tense]
          en_conj = f"{pronoun_translations[pronoun]} {eng_override}"

        else:
          en_conj = scraper.get_conjugation(verb, tense, pronoun, "en")

        current_verb_data[tense]["it"][pronoun] = it_conj
        current_verb_data[tense]["en"][pronoun] = en_conj

      verb_data[verb] = current_verb_data

    with open(output_json,'w', encoding="utf-8") as verb_output:
      verb_output.write(json.dumps(verb_data, indent=4))

    # helpers.backup_file(output_file)
    # rename(temp_output_file, output_file)

  except IOError:
    print('error: Vocab Input file does not exist')

if __name__ == "__main__":
  scrape_conjugations(OnlyMissing=True)