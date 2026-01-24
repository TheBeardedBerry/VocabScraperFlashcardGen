#!/usr/bin/env python3

import json

remaining_verbs = {
    "chiedere": {
        "infinitive": "chiedere",
        "infinitive_pronunciation": "kee-EH-deh-reh",
        "english": "to ask",
        "regular": False,
        "auxiliary": "avere",
        "present_tense": {
            "io": {"conjugation": "chiedo", "pronunciation": "kee-EH-doh", "english": "I ask", "example": "Io chiedo aiuto.", "example_english": "I ask for help."},
            "tu": {"conjugation": "chiedi", "pronunciation": "kee-EH-dee", "english": "you ask", "example": "Tu chiedi sempre.", "example_english": "You always ask."},
            "lui_lei": {"conjugation": "chiede", "pronunciation": "kee-EH-deh", "english": "he/she/it asks", "example": "Lei chiede il conto.", "example_english": "She asks for the bill."},
            "noi": {"conjugation": "chiediamo", "pronunciation": "kee-eh-dee-AH-moh", "english": "we ask", "example": "Noi chiediamo scusa.", "example_english": "We apologize."},
            "voi": {"conjugation": "chiedete", "pronunciation": "kee-eh-DEH-teh", "english": "you ask", "example": "Voi chiedete troppo.", "example_english": "You ask for too much."},
            "loro": {"conjugation": "chiedono", "pronunciation": "kee-EH-doh-noh", "english": "they ask", "example": "Loro chiedono informazioni.", "example_english": "They ask for information."}
        },
        "future_tense": {
            "io": {"conjugation": "chiederò", "pronunciation": "kee-eh-deh-ROH", "english": "I will ask", "example": "Chiederò a Maria.", "example_english": "I will ask Maria."},
            "tu": {"conjugation": "chiederai", "pronunciation": "kee-eh-deh-RAH-ee", "english": "you will ask", "example": "Tu chiederai aiuto.", "example_english": "You will ask for help."},
            "lui_lei": {"conjugation": "chiederà", "pronunciation": "kee-eh-deh-RAH", "english": "he/she/it will ask", "example": "Lei chiederà scusa.", "example_english": "She will apologize."},
            "noi": {"conjugation": "chiederemo", "pronunciation": "kee-eh-deh-REH-moh", "english": "we will ask", "example": "Chiederemo il conto.", "example_english": "We will ask for the bill."},
            "voi": {"conjugation": "chiederete", "pronunciation": "kee-eh-deh-REH-teh", "english": "you will ask", "example": "Voi chiederete tutto.", "example_english": "You will ask everything."},
            "loro": {"conjugation": "chiederanno", "pronunciation": "kee-eh-deh-RAHN-noh", "english": "they will ask", "example": "Loro chiederanno informazioni.", "example_english": "They will ask for information."}
        },
        "past_tense": {
            "io": {"conjugation": "ho chiesto", "pronunciation": "oh kee-EH-stoh", "english": "I asked", "example": "Ho chiesto aiuto.", "example_english": "I asked for help."},
            "tu": {"conjugation": "hai chiesto", "pronunciation": "AH-ee kee-EH-stoh", "english": "you asked", "example": "Hai chiesto scusa?", "example_english": "Did you apologize?"},
            "lui_lei": {"conjugation": "ha chiesto", "pronunciation": "ah kee-EH-stoh", "english": "he/she/it asked", "example": "Lei ha chiesto il conto.", "example_english": "She asked for the bill."},
            "noi": {"conjugation": "abbiamo chiesto", "pronunciation": "ahb-bee-AH-moh kee-EH-stoh", "english": "we asked", "example": "Abbiamo chiesto informazioni.", "example_english": "We asked for information."},
            "voi": {"conjugation": "avete chiesto", "pronunciation": "ah-VEH-teh kee-EH-stoh", "english": "you asked", "example": "Avete chiesto tutto?", "example_english": "Did you ask everything?"},
            "loro": {"conjugation": "hanno chiesto", "pronunciation": "AHN-noh kee-EH-stoh", "english": "they asked", "example": "Hanno chiesto aiuto.", "example_english": "They asked for help."}
        },
        "past_participle": {"form": "chiesto", "pronunciation": "kee-EH-stoh", "english": "asked"}
    },

    "scegliere": {
        "infinitive": "scegliere",
        "infinitive_pronunciation": "sheh-LYEH-reh",
        "english": "to choose",
        "regular": False,
        "auxiliary": "avere",
        "present_tense": {
            "io": {"conjugation": "scelgo", "pronunciation": "SHEL-goh", "english": "I choose", "example": "Io scelgo il menu.", "example_english": "I choose the menu."},
            "tu": {"conjugation": "scegli", "pronunciation": "SHEH-lyee", "english": "you choose", "example": "Tu scegli sempre bene.", "example_english": "You always choose well."},
            "lui_lei": {"conjugation": "sceglie", "pronunciation": "SHEH-lyeh", "english": "he/she/it chooses", "example": "Lei sceglie il vestito.", "example_english": "She chooses the dress."},
            "noi": {"conjugation": "scegliamo", "pronunciation": "sheh-lyah-moh", "english": "we choose", "example": "Noi scegliamo insieme.", "example_english": "We choose together."},
            "voi": {"conjugation": "scegliete", "pronunciation": "sheh-LYEH-teh", "english": "you choose", "example": "Voi scegliete il film?", "example_english": "Do you choose the movie?"},
            "loro": {"conjugation": "scelgono", "pronunciation": "SHEL-goh-noh", "english": "they choose", "example": "Loro scelgono il ristorante.", "example_english": "They choose the restaurant."}
        },
        "future_tense": {
            "io": {"conjugation": "sceglierò", "pronunciation": "sheh-lyeh-ROH", "english": "I will choose", "example": "Sceglierò domani.", "example_english": "I will choose tomorrow."},
            "tu": {"conjugation": "sceglierai", "pronunciation": "sheh-lyeh-RAH-ee", "english": "you will choose", "example": "Tu sceglierai bene.", "example_english": "You will choose well."},
            "lui_lei": {"conjugation": "sceglierà", "pronunciation": "sheh-lyeh-RAH", "english": "he/she/it will choose", "example": "Lei sceglierà il colore.", "example_english": "She will choose the color."},
            "noi": {"conjugation": "sceglieremo", "pronunciation": "sheh-lyeh-REH-moh", "english": "we will choose", "example": "Sceglieremo insieme.", "example_english": "We will choose together."},
            "voi": {"conjugation": "sceglierete", "pronunciation": "sheh-lyeh-REH-teh", "english": "you will choose", "example": "Voi sceglierete presto.", "example_english": "You will choose soon."},
            "loro": {"conjugation": "sceglieranno", "pronunciation": "sheh-lyeh-RAHN-noh", "english": "they will choose", "example": "Loro sceglieranno il migliore.", "example_english": "They will choose the best."}
        },
        "past_tense": {
            "io": {"conjugation": "ho scelto", "pronunciation": "oh SHEL-toh", "english": "I chose", "example": "Ho scelto il menu.", "example_english": "I chose the menu."},
            "tu": {"conjugation": "hai scelto", "pronunciation": "AH-ee SHEL-toh", "english": "you chose", "example": "Hai scelto bene.", "example_english": "You chose well."},
            "lui_lei": {"conjugation": "ha scelto", "pronunciation": "ah SHEL-toh", "english": "he/she/it chose", "example": "Lei ha scelto il vestito.", "example_english": "She chose the dress."},
            "noi": {"conjugation": "abbiamo scelto", "pronunciation": "ahb-bee-AH-moh SHEL-toh", "english": "we chose", "example": "Abbiamo scelto insieme.", "example_english": "We chose together."},
            "voi": {"conjugation": "avete scelto", "pronunciation": "ah-VEH-teh SHEL-toh", "english": "you chose", "example": "Avete scelto il film?", "example_english": "Did you choose the movie?"},
            "loro": {"conjugation": "hanno scelto", "pronunciation": "AHN-noh SHEL-toh", "english": "they chose", "example": "Hanno scelto il ristorante.", "example_english": "They chose the restaurant."}
        },
        "past_participle": {"form": "scelto", "pronunciation": "SHEL-toh", "english": "chosen"}
    }
}

# Save the remaining verbs
for verb_name, verb_data in remaining_verbs.items():
    filename = f"VerbData/individual_verbs/{verb_name}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(verb_data, f, indent=2, ensure_ascii=False)
    print(f"Completed: {filename}")

print("\nCompleted major irregular verbs!")