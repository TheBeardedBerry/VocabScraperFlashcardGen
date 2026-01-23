import requests
from bs4 import BeautifulSoup
import helpers

class VerbScraper():
    def __init__(self, lang="it"):
        self.cj_url = f"https://cooljugator.com/{lang}/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.__current_verb = None
        self.__soup = None
        self.__tenses = ["present"] #present_perfect1 preterite1 future
        self.__pronouns = {
            "io": "1",
            "tu": "2",
            "lui": "3",
            "noi": "4",
            "voi": "5",
            "loro": "6"
        }
        self.__cj_tenses = self.__cache_tense_list()


    def __cache_tense_list(self):
        tense_list = []
        for tense in self.__tenses:
            for i in list(self.__pronouns.values()):
                tense_list.append(tense + i)
        return tense_list

    def __get_url(self, verb):
        verb = helpers.remove_accents(verb)
        url = self.cj_url + verb
        self.__current_verb = verb
        print(f"{verb}: {url}")
        return url

    def __cache_cj_site_data(self, verb):
        print(verb)
        print(self.__current_verb)
        if self.__current_verb == verb:
            return self.__soup

        url = self.__get_url(verb)

        html = requests.get(url)
        self.__soup = BeautifulSoup(html.content, "html.parser")
        return self.__soup

    def __get_cj_tense(self, tense, pronoun):
        '''
        Converts the tense and pronoun to the id used for that combination in the cooljugator html.
        e.g. "present" & "io" becomes "present1"
        '''

        if tense in self.__tenses:
            return tense + self.__pronouns[pronoun]
        else:
            return None

    def get_conjugation(self, verb, tense, pronoun, lang):
        soup = self.__cache_cj_site_data(verb)

        if tense == "infinitive":
            if lang == "en":
                return soup.find(id="mainform_translation").text
            elif lang == "it":
                #I can imagine a loop happening that queries this.
                return verb

        cj_tense = self.__get_cj_tense(tense, pronoun)

        if cj_tense:
            if lang == "it":
                return soup.find(id=cj_tense).find(class_="forms-wrapper").find(class_="meta-form").text
            elif lang == "en":
                return soup.find(id=cj_tense).find(class_="forms-wrapper").find(class_="meta-translation").text
            else:
                print(f"ERROR: Couldn't find requested langauge: {lang}. Supported languages: [it, en]")
                return "NOT FOUND"
        else:
            print(f"ERROR: Couldn't find requested tense: {tense}")
            return "NOT FOUND"

    @property
    def tenses(self):
        return self.__tenses

    @property
    def pronouns(self):
        return self.__pronouns.keys()