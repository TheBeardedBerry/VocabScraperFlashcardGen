import os

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
        self.data = data
        self.italian = self.data["infinitive"]
        self.english = self.data["english"]
        self.part_of_speech = self.data["part_of_speech"]
        self.pronunciation = self.data["infinitive_pronunciation"]
        self.synonyms = self.data["synonyms"]
        self.context = self.data["context"]

        try:
            self.__gender = self.data["gender"]
        except KeyError:
            self.__gender = None

    @property
    def gender(self):
        if self.part_of_speech == "noun":
            return self.__gender
        else:
            return "N/A"

class Conjugation():
    def __init__(self, data):
        self.data = data

    @property
    def italian(self):
        return self.data["conjugation"]

    @property
    def english(self):
        return self.data["english"]

    @property
    def pronunciation(self):
        return self.data["pronunciation"]

    @property
    def example(self):
        return self.data["example"]

    @property
    def example_english(self):
        return self.data["example_english"]

class VerbTense():
    def __init__(self, tense):
        self.__tense = tense
        self.__io = Conjugation(self.__tense['io'])
        self.__tu = Conjugation(self.__tense['tu'])
        self.__lui = Conjugation(self.__tense['lui'])
        self.__noi = Conjugation(self.__tense['noi'])
        self.__voi = Conjugation(self.__tense['voi'])
        self.__loro = Conjugation(self.__tense['loro'])

    @property
    def io(self):
        return self.__io

    @property
    def tu(self):
        return self.__tu

    @property
    def lui(self):
        return self.__lui

    @property
    def noi(self):
        return self.__noi

    @property
    def voi(self):
        return self.__voi

    @property
    def loro(self):
        return self.__loro


class Verb(Word):
    def __init__(self, data):
        super().__init__(data)

        self.part_of_speech = data["part_of_speech"]
        self.presente = VerbTense(data["tenses"]["presente"])
        self.futuro_simplice = VerbTense(data["tenses"]["futuro_simplice"])
        self.passato_prossimo = VerbTense(data["tenses"]["passato_prossimo"])


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
        if not self.presente.regular:
            return IRREGULAR
        else:
            return REGULAR

# def get_verb_model(regular=True):
#     templates = []
#     fields = [{'name': 'Infinitive'},
#               {'name': 'English'},
#               {'name': 'Regular'},
#               {'name': 'Reflexive'}]
#
#     tenses = [
#         "Pres"
#     ]
#
#     pronouns = [
#         "I",
#         "You",
#         "He/She",
#         "We",
#         "You All",
#         "They"
#     ]
#
#     card_css = ".card {font-family: arial; font-size: 25px; text-align: center; color: black; background-color: white;}"
#     irregular_css = '.irregular_verb {color: red; font-size: 40px}'
#     irregular_front_css = '.irregular_front {color: red;}'
#
#     custom_css = f"{card_css} {irregular_css} {irregular_front_css}"
#
#     if regular:
#         regular_tag = 'card'
#     else:
#         regular_tag = 'irregular_verb'
#
#     templates.append({
#         'name': f'Infinitive - En->It',
#         'qfmt': f'{{{{English}}}}',
#         'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{Infinitive}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>'})
#     templates.append({
#          'name': f'Infinitive - It->En',
#          'qfmt': f'{{{{Infinitive}}}}',
#          'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{English}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b>{{{{Reflexive}}}}</b><br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>',})
#
#     for tense in tenses:
#         for pronoun in pronouns:
#             templates.append({
#                 'name': f'{tense} {pronoun} - En->It',
#                 'qfmt': f'{{{{{tense} {pronoun} - EN}}}}',
#                 'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{{tense} {pronoun} - IT}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>'})
#             templates.append({
#                 'name': f'{tense} {pronoun} - It->En',
#                 'qfmt': f'{{{{{tense} {pronoun} - IT}}}}',
#                 'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{{tense} {pronoun} - EN}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b>{{{{Reflexive}}}}</b><br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>',
#
#             })
#             fields.append({'name': f'{tense} {pronoun} - IT'})
#             fields.append({'name': f'{tense} {pronoun} - EN'})
#
#
#     if regular:
#         id = stable_id("VerbModel_stuff")
#         name = "Verbs"
#     else:
#         id = stable_id("IrregularVerbModel_Blah")
#         name = "IrregularVerbs"
#
#     return genanki.Model(
#         model_id=id,
#         name=name,
#         fields=fields,
#         templates=templates,
#         css=custom_css
#     )

def get_verb_model(json_path: str) -> genanki.Model:
    """
    Create an Anki Note Model from an Italian verb JSON definition.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = []

    # Base fields
    base_fields = [
        "Infinitive",
        "Infinitive_Pronunciation",
        "English",
        "Regular",
        "Auxiliary",
        "Part_Of_Speech",
        "Synonyms",
        "Context",
    ]

    for name in base_fields:
        fields.append({"name": name})

    # Tense / person fields
    for tense, persons in data["tenses"].items():
        for person, values in persons.items():
            prefix = f"{tense}_{person}"
            fields.extend([
                {"name": f"{prefix}_conjugation"},
                {"name": f"{prefix}_pronunciation"},
                {"name": f"{prefix}_english"},
                {"name": f"{prefix}_example"},
                {"name": f"{prefix}_example_english"},
            ])

    # Past participle fields
    fields.extend([
        {"name": "pp_form"},
        {"name": "pp_pronunciation"},
        {"name": "pp_english"},
        {"name": "pp_example"},
        {"name": "pp_example_english"},
    ])

    templates = []

    BACK_COMMON = """
    <hr>
    <div style="text-align:left">
    <b>Infinitive:</b> {{Infinitive}}<br>
    <b>Context:</b> {{Context}}<br>

    {{#Regular}}
    <b>Regular:</b> Yes
    {{/Regular}}

    {{^Regular}}
    <b style="color:red;font-size:22px">IRREGULAR VERB</b>
    {{/Regular}}
    </div>
    """

    # Infinitive cards
    templates.append({
        "name": "Infinitive En→It",
        "qfmt": "{{English}}",
        "afmt": (
                "{{FrontSide}}<hr>"
                "<div style='text-align:left'>"
                "<b>Infinitive:</b> {{Infinitive}}<br>"
                "<b>Pronunciation:</b> {{Infinitive_Pronunciation}}"
                "</div>"
                + BACK_COMMON
        ),
    })

    templates.append({
        "name": "Infinitive It→En",
        "qfmt": "{{Infinitive}}",
        "afmt": (
                "{{FrontSide}}<hr>"
                "<div style='text-align:left'>"
                "<b>English:</b> {{English}}"
                "</div>"
                + BACK_COMMON
        ),
    })

    # Conjugation cards
    for tense, persons in data["tenses"].items():
        for person in persons.keys():
            base = f"{tense}_{person}"

            back = (
                    "<div style='text-align:left'>"
                    f"<b>Tense:</b> {tense}<br>"
                    f"<b>Pronunciation:</b> {{{{{base}_pronunciation}}}}<br>"
                    f"<b>English:</b> {{{{{base}_english}}}}<br><br>"
                    f"<b>Example (IT):</b> {{{{{base}_example}}}}<br>"
                    f"<b>Example (EN):</b> {{{{{base}_example_english}}}}"
                    "</div>"
                    + BACK_COMMON
            )

            templates.append({
                "name": f"{tense} {person} En→It",
                "qfmt": f"{{{{{base}_english}}}}",
                "afmt": ("{{FrontSide}}<hr id=\"answer\">"
                        f"{{{{{base}_conjugation}}}}<br>") + back,
            })

            templates.append({
                "name": f"{tense} {person} It→En",
                "qfmt": f"{{{{{base}_conjugation}}}}",
                "afmt": ("{{FrontSide}}<hr id=\"answer\">"
                        f"{{{{{base}_english}}}}<br>") + back,
            })

    model_name = "Italian Verb – Full Conjugation"
    model_id = stable_id(model_name)

    return genanki.Model(
        model_id=model_id,
        name=model_name,
        fields=fields,
        templates=templates,
        css="""
        .card {
            font-family: Arial;
            font-size: 18px;
            text-align: center;
        }
        i {
            color: #555;
        }
        """
    )

def get_model():
    templates = []
    fields = [{'name': 'Italian'},
              {'name': 'English'},
              {'name': 'Part of Speech'},
              {'name': 'Gender'},
              {'name': 'Pronunciation'}]

    card_css = ".card {font-family: arial; font-size: 25px; text-align: center; color: black; background-color: white;}"
    irregular_css = '.irregular_verb {color: red; font-size: 40px}'
    irregular_front_css = '.irregular_front {color: red;}'

    custom_css = f"{card_css} {irregular_css} {irregular_front_css}"

    templates.append({
        'name': f'En->It',
        'qfmt': f'{{{{English}}}}',
        'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{Italian}}}}<br><br><b>Part of Speech:</b> {{{{Part of Speech}}}}<br><b><b>Gender:</b> {{{{Gender}}}}</b><br><b>Pronunciation:</b> {{{{Pronunciation}}}}'})
    templates.append({
        'name': f'It->En',
        'qfmt': f'{{{{Italian}}}}',
        'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{English}}}}<br><br><b>Part of Speech:</b> {{{{Part of Speech}}}}<br><b><b>Gender:</b> {{{{Gender}}}}</b><br><b>Pronunciation:</b> {{{{Pronunciation}}}}',

    })

    id = stable_id("WordModel_stuff")
    name = "Words"

    return genanki.Model(
        model_id=id,
        name=name,
        fields=fields,
        templates=templates,
        css=custom_css
    )

def get_anki_word_note(model, word: Word):
    return genanki.Note(guid=stable_id(f"{word.italian}{word.english}"),
                        model=model,
                        fields=[word.italian,
                                word.english,
                                word.part_of_speech,
                                word.gender,
                                word.pronunciation])

def get_anki_verb_note(model, verb: Verb):
    return genanki.Note(guid=stable_id(verb.infinitive),
                        model=model,
                        fields=[verb.infinitive,
                                verb.english,
                                verb.regular,
                                verb.reflexive,
                                verb.presente.italian.io,
                                verb.presente.english.io,
                                verb.presente.italian.tu,
                                verb.presente.english.tu,
                                verb.presente.italian.lui,
                                verb.presente.english.lui,
                                verb.presente.italian.noi,
                                verb.presente.english.noi,
                                verb.presente.italian.voi,
                                verb.presente.english.voi,
                                verb.presente.italian.loro,
                                verb.presente.english.loro])

def main(generate_verb_cards: bool = True, generate_vocab_cards: bool = True, language: str = 'Italian'):

    verb_model = get_verb_model()
    word_model = get_model()
    irregular_verb_model = get_verb_model(regular=False)
    verbs_per_deck = 10

    deck_language = language
    deck_level = "A1"


    files = os.listdir("./VocabData")

    if generate_verb_cards:
        with open(os.path.join("./VocabData", "verb_output.csv"), "r", encoding='utf-8') as f:
            lines = f.readlines()

            first_word: Verb


            deck_type = "Verbs"

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
                    unique_extension = f"{first}_{last}"
                    id_name = f"Italian::Verbs_{unique_extension}"
                    name = f"{deck_language}::{deck_level}::{deck_type}::{unique_extension}"
                    deck = genanki.Deck(
                        deck_id=stable_id(name),
                        name=name
                    )

                    for note in notes:
                        deck.add_note(note)

                    file_name = f"{deck_level}_{deck_type}_{unique_extension}.apkg"
                    genanki.Package(deck).write_to_file(os.path.join("./Decks", file_name))
                    print(f"Wrote {file_name}")
                    notes = []


    if generate_vocab_cards:
        with open(os.path.join("./VocabData", "vocab_output.csv"), "r", encoding='utf-8') as f:
            lines = f.readlines()
            model = word_model
            notes = []
            for line in lines:
                word = Word(line)
                notes.append(get_anki_word_note(model, word))

            deck_type = "Vocab"
            name = f"{deck_language}::{deck_level}::{deck_type}"
            deck = genanki.Deck(
                deck_id=stable_id(name),
                name=name
            )
            for note in notes:
                deck.add_note(note)

            file_name = f"{deck_level}_{deck_type}.apkg"
            genanki.Package(deck).write_to_file(os.path.join("./Decks", file_name))
            print(f"Wrote {file_name}")

if __name__ == "__main__":
    main(True, False)