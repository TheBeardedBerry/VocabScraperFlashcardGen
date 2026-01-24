#!/usr/bin/env python3

import json
import os
from typing import Dict, List, Tuple

class ItalianVerbGenerator:
    def __init__(self):
        # Load verb categories
        with open('VerbData/verb_categories.json', 'r', encoding='utf-8') as f:
            self.categories = json.load(f)

        # Regular verb patterns
        self.patterns = {
            'are': {
                'present': ['o', 'i', 'a', 'iamo', 'ate', 'ano'],
                'future': ['erò', 'erai', 'erà', 'eremo', 'erete', 'eranno'],
                'past_participle': 'ato'
            },
            'ere': {
                'present': ['o', 'i', 'e', 'iamo', 'ete', 'ono'],
                'future': ['erò', 'erai', 'erà', 'eremo', 'erete', 'eranno'],
                'past_participle': 'uto'
            },
            'ire_type1': {
                'present': ['o', 'i', 'e', 'iamo', 'ite', 'ono'],
                'future': ['irò', 'irai', 'irà', 'iremo', 'irete', 'iranno'],
                'past_participle': 'ito'
            },
            'ire_type2': {
                'present': ['isco', 'isci', 'isce', 'iamo', 'ite', 'iscono'],
                'future': ['irò', 'irai', 'irà', 'iremo', 'irete', 'iranno'],
                'past_participle': 'ito'
            }
        }

        self.pronouns = ['io', 'tu', 'lui_lei', 'noi', 'voi', 'loro']
        self.pronoun_translations = {
            'io': 'I',
            'tu': 'you (informal)',
            'lui_lei': 'he/she/it',
            'noi': 'we',
            'voi': 'you (plural)',
            'loro': 'they'
        }

        # Reflexive pronouns
        self.reflexive_pronouns = {
            'io': 'mi',
            'tu': 'ti',
            'lui_lei': 'si',
            'noi': 'ci',
            'voi': 'vi',
            'loro': 'si'
        }

    def get_verb_stem(self, verb: str) -> str:
        """Extract stem from infinitive"""
        if verb.endswith('arsi') or verb.endswith('ersi') or verb.endswith('irsi'):
            return verb[:-4]  # Remove -arsi, -ersi, -irsi
        elif verb.endswith('are'):
            return verb[:-3]
        elif verb.endswith('ere'):
            return verb[:-3]
        elif verb.endswith('ire'):
            return verb[:-3]
        return verb

    def get_verb_type(self, verb: str) -> str:
        """Determine verb conjugation type"""
        if verb in self.categories['classification']['regular_are']:
            return 'are'
        elif verb in self.categories['classification']['regular_ere']:
            return 'ere'
        elif verb in self.categories['classification']['regular_ire_type1']:
            return 'ire_type1'
        elif verb in self.categories['classification']['regular_ire_type2']:
            return 'ire_type2'
        elif verb in self.categories['classification']['irregular']:
            return 'irregular'
        elif verb in self.categories['classification']['reflexive']:
            return 'reflexive'
        return 'unknown'

    def is_reflexive(self, verb: str) -> bool:
        """Check if verb is reflexive"""
        return verb in self.categories['classification']['reflexive']

    def get_auxiliary(self, verb: str) -> str:
        """Get auxiliary verb (essere or avere) for past tense"""
        if verb in self.categories['auxiliary_usage']['essere']:
            return 'essere'
        else:
            return 'avere'

    def apply_spelling_changes(self, stem: str, ending: str, verb_type: str) -> str:
        """Apply Italian spelling rules"""
        # -care/-gare verbs: add 'h' before 'i'
        if stem.endswith('c') and ending.startswith('i'):
            return stem + 'h' + ending
        elif stem.endswith('g') and ending.startswith('i'):
            return stem + 'h' + ending
        # -ciare/-giare verbs: drop 'i' before endings starting with 'i'
        elif stem.endswith('ci') and ending.startswith('i'):
            return stem[:-1] + ending
        elif stem.endswith('gi') and ending.startswith('i'):
            return stem[:-1] + ending
        return stem + ending

    def conjugate_regular_verb(self, verb: str, tense: str) -> Dict:
        """Generate conjugations for regular verbs"""
        verb_type = self.get_verb_type(verb)
        if verb_type == 'irregular':
            return {}

        stem = self.get_verb_stem(verb)
        is_reflex = self.is_reflexive(verb)

        # Handle reflexive verbs - use non-reflexive stem for pattern
        pattern_type = verb_type
        if is_reflex:
            if verb.endswith('arsi'):
                pattern_type = 'are'
            elif verb.endswith('ersi'):
                pattern_type = 'ere'
            elif verb.endswith('irsi'):
                pattern_type = 'ire_type1'  # Most reflexive -ire are type 1

        if pattern_type not in self.patterns:
            return {}

        endings = self.patterns[pattern_type][tense]
        conjugations = {}

        for i, pronoun in enumerate(self.pronouns):
            ending = endings[i]
            conjugated = self.apply_spelling_changes(stem, ending, pattern_type)

            # Add reflexive pronouns if needed
            if is_reflex:
                reflex_pronoun = self.reflexive_pronouns[pronoun]
                conjugations[pronoun] = f"{reflex_pronoun} {conjugated}"
            else:
                conjugations[pronoun] = conjugated

        return conjugations

    def generate_past_tense(self, verb: str) -> Dict:
        """Generate past tense (passato prossimo)"""
        auxiliary = self.get_auxiliary(verb)
        verb_type = self.get_verb_type(verb)
        stem = self.get_verb_stem(verb)
        is_reflex = self.is_reflexive(verb)

        # Get past participle
        if verb_type == 'irregular':
            # Will need manual handling
            past_participle = "IRREGULAR"
        else:
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
            else:
                past_participle = "UNKNOWN"

        # Auxiliary conjugations (simplified)
        essere_conj = ['sono', 'sei', 'è', 'siamo', 'siete', 'sono']
        avere_conj = ['ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno']

        aux_conj = essere_conj if auxiliary == 'essere' else avere_conj
        conjugations = {}

        for i, pronoun in enumerate(self.pronouns):
            aux_verb = aux_conj[i]

            if is_reflex:
                reflex_pronoun = self.reflexive_pronouns[pronoun]
                if auxiliary == 'essere':
                    # Agreement with essere
                    conjugations[pronoun] = f"{reflex_pronoun} {aux_verb} {past_participle}/a"
                else:
                    conjugations[pronoun] = f"{reflex_pronoun} {aux_verb} {past_participle}"
            else:
                if auxiliary == 'essere':
                    # Agreement with essere
                    conjugations[pronoun] = f"{aux_verb} {past_participle}/a"
                else:
                    conjugations[pronoun] = f"{aux_verb} {past_participle}"

        return conjugations

    def generate_pronunciation(self, word: str) -> str:
        """Generate simplified pronunciation for English speakers"""
        # Basic Italian pronunciation rules
        pronunciation = word.lower()

        # Replace common patterns
        replacements = {
            'ch': 'k', 'gh': 'g', 'sc': 'sh', 'gn': 'ny', 'gl': 'ly',
            'ci': 'chee', 'ce': 'cheh', 'gi': 'jee', 'ge': 'jeh',
            'a': 'ah', 'e': 'eh', 'i': 'ee', 'o': 'oh', 'u': 'oo'
        }

        for italian, english in replacements.items():
            pronunciation = pronunciation.replace(italian, english)

        # Capitalize stressed syllable (simplified - usually second-to-last)
        words = pronunciation.split()
        if words:
            main_word = words[-1]  # Last word for compound forms
            if len(main_word) > 3:
                # Simple stress rule: stress second-to-last syllable
                stressed = main_word.upper()
                pronunciation = pronunciation.replace(main_word, stressed)

        return pronunciation

def main():
    generator = ItalianVerbGenerator()

    # Test with a few regular verbs
    test_verbs = ['abitare', 'credere', 'finire', 'alzarsi']

    for verb in test_verbs:
        print(f"\n=== {verb} ===")
        print(f"Type: {generator.get_verb_type(verb)}")
        print(f"Auxiliary: {generator.get_auxiliary(verb)}")
        print(f"Reflexive: {generator.is_reflexive(verb)}")

        present = generator.conjugate_regular_verb(verb, 'present')
        future = generator.conjugate_regular_verb(verb, 'future')
        past = generator.generate_past_tense(verb)

        print("Present:", present)
        print("Future:", future)
        print("Past:", past)

if __name__ == "__main__":
    main()