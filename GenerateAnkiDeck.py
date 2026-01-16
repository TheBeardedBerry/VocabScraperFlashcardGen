import os

import italian_dictionary as it_dict
import genanki
import hashlib
import json

#TODO: Get List of A1 words
#TODO: Get data for all A1 words
#TODO: Create cards for non-verbs
#TODO: Create classes to manage non-verbs
#TODO: Account for missing verb conjugations. Not all verbs have all 6
#TODO: Account for other verb endings

with open('patterns/verbs.json') as verb_pattern_file:
    VERB_PATTERNS = json.load(verb_pattern_file)

VERB_ENDINGS = VERB_PATTERNS['endings']
REGULAR = "Regular"
IRREGULAR = "Irregular"
REFLEXIVE = "Reflexive"
NOTREFLEXIVE = "NotReflexive"

def stable_id(name: str) -> int:
    """
    Generate a stable deck ID based on MD5 of name.

    Note: MD5 is used here for generating stable IDs, not for security purposes.

    Args:
        name: String to hash

    Returns:
        Integer ID derived from first 10 hex digits of MD5 hash
    """
    # The usedforsecurity parameter is available in Python 3.9+
    # but mypy might not recognize it, so we use type: ignore
    # This is explicitly not used for security purposes, only for generating stable IDs
    digest = hashlib.md5(name.encode("utf-8"), usedforsecurity=False).hexdigest()  # type: ignore
    return int(digest[:10], 16)

class Word():
    def __init__(self, data):
        self.data = data.split(",")
        self.italian = self.data[0]
        self.english = self.data[1]

class VerbLang():
    def __init__(self, io=None, tu=None, lui_lei=None, noi=None, voi=None, loro=None, reflexive=None):
        self.__io = io
        self.__tu = tu
        self.__lui_lei = lui_lei
        self.__noi = noi
        self.__voi = voi
        self.__loro = loro
        self.__reflexive = reflexive

    @property
    def io(self):
        if self.__reflexive == REFLEXIVE and self.__io.startswith("I "):
            return f"{self.__io} myself"
        return self.__io

    @property
    def tu(self):
        if self.__reflexive == REFLEXIVE and self.__tu.startswith("You"):
            return f"{self.__tu} yourself"
        return self.__tu

    @property
    def lui_lei(self):
        if self.__reflexive == REFLEXIVE and self.__lui_lei.startswith("He"):
            return f"{self.__lui_lei} him/her/itself"
        return self.__lui_lei

    @property
    def noi(self):
        if self.__reflexive == REFLEXIVE and self.__noi.startswith("We"):
            return f"{self.__noi} ourselves"
        return self.__noi

    @property
    def voi(self):
        if self.__reflexive == REFLEXIVE and self.__voi.startswith("You all"):
            return f"{self.__voi} yourselves"
        return self.__voi

    @property
    def loro(self):
        if self.__reflexive == REFLEXIVE and self.__loro.startswith("They"):
            return f"{self.__loro} themselves"
        return self.__loro


class VerbTense():
    def __init__(self, tense=None, ending=None, reflexive=None, io=None, i=None, tu=None, you=None, lui_lei=None, he_she=None, noi=None, we=None, voi=None, you_all=None, loro=None, they=None):
        self.english = VerbLang(i, you, he_she, we, you_all, they, reflexive)
        self.italian = VerbLang(io, tu, lui_lei, noi, voi, loro, reflexive)
        self.tense = tense
        self.ending = ending

    @property
    def regular(self):
        regular_endings = VERB_PATTERNS[self.tense][self.ending]

        if not self.italian.io.endswith(regular_endings['io']):
            return False
        elif not self.italian.tu.endswith(regular_endings['tu']):
            return False
        elif not self.italian.lui_lei.endswith(regular_endings['lui/lei']):
            return False
        elif not self.italian.noi.endswith(regular_endings['noi']):
            return False
        elif not self.italian.voi.endswith(regular_endings['voi']):
            return False
        elif not self.italian.loro.endswith(regular_endings['loro']):
            return False
        else:
            return True


class Verb(Word):
    def __init__(self, data):
        super().__init__(data)

        self.part_of_speech = "Verb"
        self.present = VerbTense("present", self.ending, self.reflexive,
                                 self.data[2], self.data[3],   #I
                                 self.data[4], self.data[5],   #You
                                 self.data[6], self.data[7],   #HeSheIt
                                 self.data[8], self.data[9],   #We
                                 self.data[10], self.data[11], #YouAll
                                 self.data[12], self.data[13]) #They


    @property
    def infinitive(self) -> str:
        return self.italian

    @property
    def ending(self) -> str:
        endings = VERB_ENDINGS["standard"] + VERB_ENDINGS["reflexive"]
        for verb_ending in endings:
            if self.infinitive.endswith(verb_ending):
                return verb_ending
        else:
            print(f"{self.infinitive} doesnt have a known ending")
            return None

    @property
    def reflexive(self) -> bool:
        if self.ending in VERB_ENDINGS["reflexive"]:
            return REFLEXIVE
        else:
            return NOTREFLEXIVE

    @property
    def stem(self) -> str:
        return self.infinitive.rstrip(self.ending)

    @property
    def regular(self) -> bool:
        if not self.present.regular:
            return IRREGULAR
        else:
            return REGULAR

def get_verb_model(regular=True):
    templates = []
    fields = [{'name': 'Infinitive'},
              {'name': 'English'},
              {'name': 'Regular'},
              {'name': 'Reflexive'}]

    tenses = [
        "Pres"
    ]

    pronouns = [
        "I",
        "You",
        "He/She",
        "We",
        "You All",
        "They"
    ]

    card_css = ".card {font-family: arial; font-size: 25px; text-align: center; color: black; background-color: white;}"
    irregular_css = '.irregular_verb {color: red; font-size: 40px}'
    irregular_front_css = '.irregular_front {color: red;}'

    custom_css = f"{card_css} {irregular_css} {irregular_front_css}"

    if regular:
        regular_tag = 'card'
    else:
        regular_tag = 'irregular_verb'


    for tense in tenses:
        for pronoun in pronouns:
            templates.append({
                'name': f'{tense} {pronoun} - En->It',
                'qfmt': f'{{{{{tense} {pronoun} - EN}}}}',
                'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{{tense} {pronoun} - IT}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>'})
            templates.append({
                'name': f'{tense} {pronoun} - It->En',
                'qfmt': f'{{{{{tense} {pronoun} - IT}}}}',
                'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{{tense} {pronoun} - EN}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b>{{{{Reflexive}}}}</b><br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>',

            })
            fields.append({'name': f'{tense} {pronoun} - IT'})
            fields.append({'name': f'{tense} {pronoun} - EN'})

    if regular:
        id = stable_id("VerbModel_stuff")
        name = "Verbs"
    else:
        id = stable_id("IrregularVerbModel_Blah")
        name = "IrregularVerbs"

    return genanki.Model(
        model_id=id,
        name=name,
        fields=fields,
        templates=templates,
        css=custom_css
    )

def get_anki_verb_note(model, verb: Verb):
    return genanki.Note(guid=stable_id(verb.infinitive),
                        model=model,
                        fields=[verb.infinitive,
                                verb.english,
                                verb.regular,
                                verb.reflexive,
                                verb.present.italian.io,
                                verb.present.english.io,
                                verb.present.italian.tu,
                                verb.present.english.tu,
                                verb.present.italian.lui_lei,
                                verb.present.english.lui_lei,
                                verb.present.italian.noi,
                                verb.present.english.noi,
                                verb.present.italian.voi,
                                verb.present.english.voi,
                                verb.present.italian.loro,
                                verb.present.english.loro])

def main():

    verb_model = get_verb_model()
    irregular_verb_model = get_verb_model(regular=False)
    verbs_per_deck = 10

    files = os.listdir("./VocabData")
    deck = genanki.Deck(
        deck_id=1260383378,
        name="ItalianVocab")

    for file in files:
        with open(os.path.join("./VocabData", file), "r", encoding='utf-8') as f:
            lines = f.readlines()

            first_word: Verb

            notes = []
            for line in lines:

                print(line)

                verb = Verb(line)

                if verb.regular == REGULAR:
                    model = verb_model
                else:
                    model = irregular_verb_model

                if len(notes) == 0:
                    first_word = verb

                notes.append(get_anki_verb_note(model, verb))

                if len(notes) >= verbs_per_deck or line == lines[-1]:
                    first = first_word.infinitive
                    last = verb.infinitive
                    unique_extension = f"Verbs_{first}_{last}"
                    name = f"ItalianVocab::{unique_extension}"
                    deck = genanki.Deck(
                        deck_id=stable_id(name),
                        name=name
                    )

                    for note in notes:
                        deck.add_note(note)

                    genanki.Package(deck).write_to_file(os.path.join("./Decks", f"{unique_extension}.apkg"))
                    print(f"Wrote {unique_extension}.apkg")
                    notes = []

if __name__ == "__main__":
    main()