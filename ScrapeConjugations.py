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

# read in url-list
try:
  with open('A1_Verbs.txt') as vocab_input:
    vocab_search = []
    vocab_search = [line.rstrip() for line in vocab_input]

    # create empty data list
    data = []

  # loop through vocab input
  for i in vocab_search:
    url = "https://cooljugator.com/it/" + i
    print(f"{i}: {url}")

    # note search vocab to output data list
    data.append(i)
    data.append(",") # insert a tab

    # download content from the web url
    try:
      html = requests.get(url)
      soup = BeautifulSoup(html.content, "html.parser")
      
      search = ["present1", "present2", "present3", "present4", "present5", "present6"]#, "past1", "past2", "past3", "past4", "past5", "past6"]
              #present_perfect1
              #preterite1
              #future1
      english = soup.find(id="mainform_translation").text
      data.append(english)
      data.append(",")

      # scrape the online data
      for j in search:
        conjug = soup.find(id=j).find(class_="forms-wrapper").find(class_="meta-form").text
        conjug_eng = soup.find(id=j).find(class_="forms-wrapper").find(class_="meta-translation").text

        #print(conjug)
        data.append(conjug) # append to existing data
        data.append(",") # insert a tab
        data.append(conjug_eng)
        data.append(",")


    except:
      print('error: No online data found')

    data.append("\n")

    vocab_output = open('VocabData/verb_output.csv','w', encoding="utf-8")
    
    for x in range(len(data)):
      #print(data[x])
      vocab_output.write(data[x])

    vocab_output.close()

except IOError:
  print('error: Vocab Input file does not exist')

# EOF
