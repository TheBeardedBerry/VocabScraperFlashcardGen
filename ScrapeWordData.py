#!/usr/bin/env python3

#packages to install:
# pip install soupsieve
# pip install beautifulsoup4
# pip install bs4
# pip install dnspython
# pip install pymongo

import requests, unicodedata  # lib to make web requests
from random import randint
from time import sleep
import json
from bs4 import BeautifulSoup
import utils
from os import rename

def remove_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

#
# url = "https://dictionary.cambridge.org/dictionary/italian-english/bello"
#
# html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
# soup = BeautifulSoup(html.content, "html.parser")
#
#
# english = soup.find(id="page-content").find(class_="trans dtrans lmr--5").text
# part_of_speech = soup.find(id="page-content").find(class_="pos dpos").text
# gender = soup.find(id="page-content").find(class_="gc dgc").text
# pronunciation = soup.find(id="page-content").find(class_="ipa dipa").text
#
# print(f"English: {english}, Part of Speech: {part_of_speech}, Gender: {gender}, Pronunciation: {pronunciation}")
#
# quit()
# read in url-list
output_file = "VocabData/vocab_output.csv"
temp_output_file = "VocabData/temp_vocab_output.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
genders = ["feminine", "masculine"]

try:
  with open('A1_Vocab.csv', encoding="utf-8") as vocab_input:
    vocab_search = []
    vocab_search = vocab_input.readlines()

    # create empty data list
    data = []

  # loop through vocab input
  for line in vocab_search:

    terms = line.split(",")
    i = terms[0].strip()
    english = terms[1]

    url_i = i.split('/')[0]
    url = "https://dictionary.cambridge.org/dictionary/italian-english/" + url_i.replace(' ', '-').lower()
    url = remove_accents(url)
    print(f"{i}: {url}")

    # note search vocab to output data list
    data.append(i)
    data.append(",") # insert a tab
    data.append(english)
    data.append(",")

    # download content from the web url
    try:
      sleep(randint(1, 3))
      html = requests.get(url, headers=headers)
      soup = BeautifulSoup(html.content, "html.parser")

      #english = soup.find(id="page-content").find(class_="trans dtrans lmr--5").text

      try:
        gender = soup.find(id="page-content").find(class_="gram dgram").find(class_="gc dgc").text
      except AttributeError:
        gender = "N/A"

      try:
        pronunciation = soup.find(id="page-content").find(class_="ipa dipa").text
      except AttributeError:
        pronunciation = "Not Found"

      try:
        part_of_speech = soup.find(id="page-content").find(class_="pos dpos").text
        data.append(part_of_speech)
      except AttributeError:
        part_of_speech = "Not Found"

      data.append(",")

      if part_of_speech:
        if part_of_speech == "noun":
          data.append(gender)
        else:
          data.append("N/A")
      else:
        data.append("N/A")
      data.append(",")

      data.append(pronunciation)

      data.append("\n")

    except:
      data.append("\n")
      print('error: No online data found')



    vocab_output = open(temp_output_file, 'w', encoding="utf-8")

    for x in range(len(data)):
      #print(data[x])
      vocab_output.write(data[x])

    vocab_output.close()

  utils.backup_file(output_file)
  rename(temp_output_file, output_file)
except IOError:

  print('error: Vocab Input file does not exist')

# EOF
