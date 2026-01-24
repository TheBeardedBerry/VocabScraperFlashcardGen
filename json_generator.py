#!/usr/bin/env python3

import json
import os
from verb_generator import ItalianVerbGenerator

class VerbJSONGenerator(ItalianVerbGenerator):
    def __init__(self):
        super().__init__()

        # English translations for common verbs
        self.verb_translations = {
            'abitare': 'to live/to dwell',
            'aiutare': 'to help',
            'alzarsi': 'to get up/to wake up',
            'amare': 'to love',
            'andare': 'to go',
            'aprire': 'to open',
            'arrivare': 'to arrive',
            'ascoltare': 'to listen',
            'aspettare': 'to wait',
            'avere': 'to have',
            'ballare': 'to dance',
            'bere': 'to drink',
            'cambiare': 'to change',
            'camminare': 'to walk',
            'cantare': 'to sing',
            'capire': 'to understand',
            'cavalcare': 'to ride (a horse)',
            'cenare': 'to have dinner',
            'cercare': 'to look for',
            'chiamare': 'to call',
            'chiedere': 'to ask',
            'chiudere': 'to close',
            'cominciare': 'to begin',
            'comprare': 'to buy',
            'conoscere': 'to know/to meet',
            'controllare': 'to check/to control',
            'correre': 'to run',
            'costare': 'to cost',
            'creare': 'to create',
            'credere': 'to believe',
            'cucinare': 'to cook',
            'danzare': 'to dance',
            'dare': 'to give',
            'dimenticare': 'to forget',
            'dire': 'to say/to tell',
            'disegnare': 'to draw',
            'divertirsi': 'to have fun',
            'entrare': 'to enter',
            'essere': 'to be',
            'fare': 'to do/to make',
            'fermare': 'to stop',
            'finire': 'to finish',
            'fumare': 'to smoke',
            'giocare': 'to play',
            'guardare': 'to watch/to look at',
            'guidare': 'to drive',
            'imparare': 'to learn',
            'incontrare': 'to meet',
            'indossare': 'to wear',
            'iniziare': 'to start',
            'insegnare': 'to teach',
            'inviare': 'to send',
            'invitare': 'to invite',
            'lasciare': 'to leave/to let',
            'lavare': 'to wash',
            'lavorare': 'to work',
            'leggere': 'to read',
            'mandare': 'to send',
            'mangiare': 'to eat',
            'mettere': 'to put',
            'morire': 'to die',
            'mostrare': 'to show',
            'nuotare': 'to swim',
            'ottenere': 'to get/to obtain',
            'pagare': 'to pay',
            'parcheggiare': 'to park',
            'parlare': 'to speak/to talk',
            'partire': 'to leave/to depart',
            'pensare': 'to think',
            'piacere': 'to like/to please',
            'piovere': 'to rain',
            'portare': 'to bring/to carry',
            'potere': 'to be able to/can',
            'pranzare': 'to have lunch',
            'prendere': 'to take',
            'preoccuparsi': 'to worry',
            'pulire': 'to clean',
            'ricordare': 'to remember',
            'ridere': 'to laugh',
            'rispondere': 'to answer',
            'scegliere': 'to choose',
            'scrivere': 'to write',
            'scusarsi': 'to apologize',
            'sedersi': 'to sit down',
            'sentire': 'to hear/to feel',
            'stare': 'to stay/to be',
            'studiare': 'to study',
            'suonare': 'to play (instrument)',
            'svegliarsi': 'to wake up',
            'telefonare': 'to phone',
            'uscire': 'to go out',
            'usare': 'to use',
            'vedere': 'to see',
            'venire': 'to come',
            'viaggiare': 'to travel',
            'visitare': 'to visit',
            'vivere': 'to live',
            'volare': 'to fly',
            'volere': 'to want'
        }

        # A1-level example sentence templates
        self.example_templates = {
            'io': {
                'abitare': ("Io abito a Roma.", "I live in Rome."),
                'lavorare': ("Io lavoro in ufficio.", "I work in an office."),
                'studiare': ("Io studio italiano.", "I study Italian."),
                'mangiare': ("Io mangio la pizza.", "I eat pizza."),
                'essere': ("Io sono italiano.", "I am Italian."),
                'avere': ("Io ho vent'anni.", "I am twenty years old."),
                'default': ("Io {} ogni giorno.", "I {} every day.")
            },
            'tu': {
                'abitare': ("Tu abiti vicino alla scuola?", "Do you live near the school?"),
                'lavorare': ("Tu lavori il sabato?", "Do you work on Saturday?"),
                'parlare': ("Tu parli inglese?", "Do you speak English?"),
                'essere': ("Tu sei molto gentile.", "You are very kind."),
                'avere': ("Tu hai una macchina?", "Do you have a car?"),
                'default': ("Tu {} bene.", "You {} well.")
            },
            'lui_lei': {
                'abitare': ("Lei abita in centro.", "She lives downtown."),
                'lavorare': ("Lui lavora in banca.", "He works at a bank."),
                'essere': ("Lei è una dottoressa.", "She is a doctor."),
                'avere': ("Lui ha due figli.", "He has two children."),
                'default': ("Lei {} molto.", "She {} a lot.")
            },
            'noi': {
                'abitare': ("Noi abitiamo insieme.", "We live together."),
                'studiare': ("Noi studiamo all'università.", "We study at university."),
                'essere': ("Noi siamo studenti.", "We are students."),
                'avere': ("Noi abbiamo fame.", "We are hungry."),
                'default': ("Noi {} insieme.", "We {} together.")
            },
            'voi': {
                'abitare': ("Voi abitate qui?", "Do you live here?"),
                'essere': ("Voi siete pronti?", "Are you ready?"),
                'avere': ("Voi avete tempo?", "Do you have time?"),
                'default': ("Voi {} bene?", "Do you {} well?")
            },
            'loro': {
                'abitare': ("Loro abitano in Italia.", "They live in Italy."),
                'essere': ("Loro sono amici.", "They are friends."),
                'avere': ("Loro hanno una casa.", "They have a house."),
                'default': ("Loro {} spesso.", "They {} often.")
            }
        }

    def generate_pronunciation_detailed(self, word: str) -> str:
        """Enhanced pronunciation generator"""
        pronunciation = word.lower()

        # Handle common Italian patterns more accurately
        replacements = [
            ('sce', 'sheh'), ('sci', 'shee'),
            ('che', 'keh'), ('chi', 'kee'),
            ('ghe', 'geh'), ('ghi', 'gee'),
            ('gn', 'ny'), ('gl', 'ly'),
            ('cia', 'chah'), ('cio', 'choh'), ('ciu', 'choo'),
            ('gia', 'jah'), ('gio', 'joh'), ('giu', 'joo'),
            ('cc', 'k'), ('gg', 'g'),
            ('rr', 'rr'), ('ll', 'll'),  # Keep double consonants
            ('qu', 'kw')
        ]

        for italian, english in replacements:
            pronunciation = pronunciation.replace(italian, english)

        # Replace individual vowels last
        vowel_replacements = [
            ('a', 'ah'), ('e', 'eh'), ('i', 'ee'), ('o', 'oh'), ('u', 'oo')
        ]

        for italian, english in vowel_replacements:
            pronunciation = pronunciation.replace(italian, english)

        # Simple stress marking (capitalize stressed syllable)
        syllables = pronunciation.split()
        if syllables and len(syllables[0]) > 2:
            # Most Italian words stress the second-to-last syllable
            word = syllables[0]
            if len(word) > 4:
                # Find approximate stressed syllable
                mid = len(word) // 2
                stressed = word[:mid].upper() + word[mid:]
                pronunciation = stressed

        return pronunciation

    def get_example_sentence(self, verb: str, pronoun: str, conjugation: str, tense: str) -> tuple:
        """Generate A1-appropriate example sentences"""
        # Check for specific examples first
        if pronoun in self.example_templates and verb in self.example_templates[pronoun]:
            return self.example_templates[pronoun][verb]

        # Use default templates
        if pronoun in self.example_templates:
            template_it, template_en = self.example_templates[pronoun]['default']

            # Simple verb substitution
            italian_example = template_it.format(conjugation) if '{}' in template_it else f"{template_it} {conjugation}."

            # English translation
            verb_translation = self.verb_translations.get(verb, verb)
            english_base = verb_translation.replace('to ', '')
            english_example = template_en.format(english_base) if '{}' in template_en else f"{template_en} {english_base}."

            return (italian_example, english_example)

        # Fallback
        return (f"Io {conjugation}.", f"I {verb}.")

    def generate_complete_verb_json(self, verb: str) -> dict:
        """Generate complete JSON structure for a verb"""
        verb_type = self.get_verb_type(verb)
        is_reflex = self.is_reflexive(verb)
        auxiliary = self.get_auxiliary(verb)

        # Base verb info
        verb_data = {
            "infinitive": verb,
            "infinitive_pronunciation": self.generate_pronunciation_detailed(verb),
            "english": self.verb_translations.get(verb, f"to {verb}"),
            "regular": verb_type != 'irregular',
            "auxiliary": auxiliary
        }

        if is_reflex:
            verb_data["reflexive"] = True

        # Generate conjugations for all tenses
        tenses = ['present', 'future']

        for tense in tenses:
            if verb_type == 'irregular':
                # Skip regular conjugation for irregular verbs
                verb_data[f"{tense}_tense"] = "IRREGULAR - MANUAL INPUT NEEDED"
                continue

            conjugations = self.conjugate_regular_verb(verb, tense)
            tense_data = {}

            for pronoun, conjugation in conjugations.items():
                pronunciation = self.generate_pronunciation_detailed(conjugation)

                # English translation for pronoun + tense
                pronoun_en = self.pronoun_translations[pronoun]
                verb_en_base = self.verb_translations.get(verb, verb).replace('to ', '')

                if tense == 'present':
                    if pronoun == 'io':
                        english_trans = f"I {verb_en_base}"
                    elif pronoun == 'tu':
                        english_trans = f"you {verb_en_base}"
                    elif pronoun == 'lui_lei':
                        english_trans = f"he/she/it {verb_en_base}s"
                    elif pronoun == 'noi':
                        english_trans = f"we {verb_en_base}"
                    elif pronoun == 'voi':
                        english_trans = f"you {verb_en_base}"
                    elif pronoun == 'loro':
                        english_trans = f"they {verb_en_base}"
                elif tense == 'future':
                    english_trans = f"{pronoun_en} will {verb_en_base}"

                # Get example sentence
                example_it, example_en = self.get_example_sentence(verb, pronoun, conjugation, tense)

                tense_data[pronoun] = {
                    "conjugation": conjugation,
                    "pronunciation": pronunciation,
                    "english": english_trans,
                    "example": example_it,
                    "example_english": example_en
                }

            verb_data[f"{tense}_tense"] = tense_data

        # Add past tense
        past_conjugations = self.generate_past_tense(verb)
        if verb_type != 'irregular':
            past_tense_data = {}
            for pronoun, conjugation in past_conjugations.items():
                pronunciation = self.generate_pronunciation_detailed(conjugation)

                # English for past
                pronoun_en = self.pronoun_translations[pronoun]
                verb_en_base = self.verb_translations.get(verb, verb).replace('to ', '')
                english_trans = f"{pronoun_en} {verb_en_base}ed" if not verb_en_base.endswith('e') else f"{pronoun_en} {verb_en_base}d"

                # Simple past example
                example_it = f"Ieri {conjugation}."
                example_en = f"Yesterday {english_trans.lower()}."

                past_tense_data[pronoun] = {
                    "conjugation": conjugation,
                    "pronunciation": pronunciation,
                    "english": english_trans,
                    "example": example_it,
                    "example_english": example_en
                }
            verb_data["past_tense"] = past_tense_data
        else:
            verb_data["past_tense"] = "IRREGULAR - MANUAL INPUT NEEDED"

        # Past participle
        if verb_type != 'irregular':
            stem = self.get_verb_stem(verb)
            pattern_type = verb_type
            if is_reflex:
                if verb.endswith('arsi'):
                    pattern_type = 'are'
                elif verb.endswith('ersi'):
                    pattern_type = 'ere'
                elif verb.endswith('irsi'):
                    pattern_type = 'ire_type1'

            if pattern_type in self.patterns:
                pp_ending = self.patterns[pattern_type]['past_participle']
                past_participle = stem + pp_ending

                verb_data["past_participle"] = {
                    "form": past_participle + ("/a" if auxiliary == "essere" else ""),
                    "pronunciation": self.generate_pronunciation_detailed(past_participle),
                    "english": f"{verb_en_base}ed" if not verb_en_base.endswith('e') else f"{verb_en_base}d"
                }
        else:
            verb_data["past_participle"] = "IRREGULAR - MANUAL INPUT NEEDED"

        return verb_data

    def save_verb_json(self, verb: str):
        """Generate and save individual verb JSON file"""
        verb_data = self.generate_complete_verb_json(verb)

        filename = f"VerbData/individual_verbs/{verb}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(verb_data, f, indent=2, ensure_ascii=False)

        print(f"Generated: {filename}")

def main():
    generator = VerbJSONGenerator()

    # Generate first few regular -are verbs
    regular_are_verbs = generator.categories['classification']['regular_are'][:5]

    for verb in regular_are_verbs:
        generator.save_verb_json(verb)

if __name__ == "__main__":
    main()