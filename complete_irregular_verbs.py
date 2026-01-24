#!/usr/bin/env python3

import json

# Complete conjugation data for all irregular verbs
irregular_verbs_data = {
    "andare": {
        "infinitive": "andare",
        "infinitive_pronunciation": "ahn-DAH-reh",
        "english": "to go",
        "regular": False,
        "auxiliary": "essere",
        "present_tense": {
            "io": {"conjugation": "vado", "pronunciation": "VAH-doh", "english": "I go", "example": "Io vado a casa.", "example_english": "I go home."},
            "tu": {"conjugation": "vai", "pronunciation": "VAH-ee", "english": "you go", "example": "Tu vai al lavoro?", "example_english": "Do you go to work?"},
            "lui_lei": {"conjugation": "va", "pronunciation": "vah", "english": "he/she/it goes", "example": "Lei va in Italia.", "example_english": "She goes to Italy."},
            "noi": {"conjugation": "andiamo", "pronunciation": "ahn-dee-AH-moh", "english": "we go", "example": "Noi andiamo al cinema.", "example_english": "We go to the cinema."},
            "voi": {"conjugation": "andate", "pronunciation": "ahn-DAH-teh", "english": "you go", "example": "Voi andate a scuola?", "example_english": "Do you go to school?"},
            "loro": {"conjugation": "vanno", "pronunciation": "VAHN-noh", "english": "they go", "example": "Loro vanno in vacanza.", "example_english": "They go on vacation."}
        },
        "future_tense": {
            "io": {"conjugation": "andrò", "pronunciation": "ahn-DROH", "english": "I will go", "example": "Andrò al mare domani.", "example_english": "I will go to the sea tomorrow."},
            "tu": {"conjugation": "andrai", "pronunciation": "ahn-DRAH-ee", "english": "you will go", "example": "Tu andrai all'università.", "example_english": "You will go to university."},
            "lui_lei": {"conjugation": "andrà", "pronunciation": "ahn-DRAH", "english": "he/she/it will go", "example": "Lei andrà a Parigi.", "example_english": "She will go to Paris."},
            "noi": {"conjugation": "andremo", "pronunciation": "ahn-DREH-moh", "english": "we will go", "example": "Andremo insieme.", "example_english": "We will go together."},
            "voi": {"conjugation": "andrete", "pronunciation": "ahn-DREH-teh", "english": "you will go", "example": "Voi andrete presto?", "example_english": "Will you go soon?"},
            "loro": {"conjugation": "andranno", "pronunciation": "ahn-DRAHN-noh", "english": "they will go", "example": "Loro andranno via.", "example_english": "They will go away."}
        },
        "past_tense": {
            "io": {"conjugation": "sono andato/a", "pronunciation": "SOH-noh ahn-DAH-toh/tah", "english": "I went/have gone", "example": "Sono andato al supermercato.", "example_english": "I went to the supermarket."},
            "tu": {"conjugation": "sei andato/a", "pronunciation": "say ahn-DAH-toh/tah", "english": "you went/have gone", "example": "Sei andato al lavoro ieri?", "example_english": "Did you go to work yesterday?"},
            "lui_lei": {"conjugation": "è andato/a", "pronunciation": "eh ahn-DAH-toh/tah", "english": "he/she/it went/has gone", "example": "È andata a casa.", "example_english": "She went home."},
            "noi": {"conjugation": "siamo andati/e", "pronunciation": "see-AH-moh ahn-DAH-tee/teh", "english": "we went/have gone", "example": "Siamo andati al ristorante.", "example_english": "We went to the restaurant."},
            "voi": {"conjugation": "siete andati/e", "pronunciation": "see-EH-teh ahn-DAH-tee/teh", "english": "you went/have gone", "example": "Siete andati in vacanza?", "example_english": "Did you go on vacation?"},
            "loro": {"conjugation": "sono andati/e", "pronunciation": "SOH-noh ahn-DAH-tee/teh", "english": "they went/have gone", "example": "Sono andati via.", "example_english": "They went away."}
        },
        "past_participle": {"form": "andato/a/i/e", "pronunciation": "ahn-DAH-toh/tah/tee/teh", "english": "gone"}
    },

    "fare": {
        "infinitive": "fare",
        "infinitive_pronunciation": "FAH-reh",
        "english": "to do/to make",
        "regular": False,
        "auxiliary": "avere",
        "present_tense": {
            "io": {"conjugation": "faccio", "pronunciation": "FAHT-choh", "english": "I do/make", "example": "Io faccio colazione.", "example_english": "I have breakfast."},
            "tu": {"conjugation": "fai", "pronunciation": "FAH-ee", "english": "you do/make", "example": "Tu fai sport?", "example_english": "Do you do sports?"},
            "lui_lei": {"conjugation": "fa", "pronunciation": "fah", "english": "he/she/it does/makes", "example": "Lei fa la dottoressa.", "example_english": "She is a doctor."},
            "noi": {"conjugation": "facciamo", "pronunciation": "faht-CHAH-moh", "english": "we do/make", "example": "Noi facciamo i compiti.", "example_english": "We do homework."},
            "voi": {"conjugation": "fate", "pronunciation": "FAH-teh", "english": "you do/make", "example": "Voi fate tutto bene.", "example_english": "You do everything well."},
            "loro": {"conjugation": "fanno", "pronunciation": "FAHN-noh", "english": "they do/make", "example": "Loro fanno una festa.", "example_english": "They have a party."}
        },
        "future_tense": {
            "io": {"conjugation": "farò", "pronunciation": "fah-ROH", "english": "I will do/make", "example": "Farò del mio meglio.", "example_english": "I will do my best."},
            "tu": {"conjugation": "farai", "pronunciation": "fah-RAH-ee", "english": "you will do/make", "example": "Tu farai un viaggio.", "example_english": "You will take a trip."},
            "lui_lei": {"conjugation": "farà", "pronunciation": "fah-RAH", "english": "he/she/it will do/make", "example": "Lei farà una torta.", "example_english": "She will make a cake."},
            "noi": {"conjugation": "faremo", "pronunciation": "fah-REH-moh", "english": "we will do/make", "example": "Faremo una passeggiata.", "example_english": "We will take a walk."},
            "voi": {"conjugation": "farete", "pronunciation": "fah-REH-teh", "english": "you will do/make", "example": "Voi farete un buon lavoro.", "example_english": "You will do a good job."},
            "loro": {"conjugation": "faranno", "pronunciation": "fah-RAHN-noh", "english": "they will do/make", "example": "Loro faranno tardi.", "example_english": "They will be late."}
        },
        "past_tense": {
            "io": {"conjugation": "ho fatto", "pronunciation": "oh FAHT-toh", "english": "I did/have done", "example": "Ho fatto i compiti.", "example_english": "I did my homework."},
            "tu": {"conjugation": "hai fatto", "pronunciation": "AH-ee FAHT-toh", "english": "you did/have done", "example": "Hai fatto bene.", "example_english": "You did well."},
            "lui_lei": {"conjugation": "ha fatto", "pronunciation": "ah FAHT-toh", "english": "he/she/it did/has done", "example": "Lei ha fatto una torta.", "example_english": "She made a cake."},
            "noi": {"conjugation": "abbiamo fatto", "pronunciation": "ahb-bee-AH-moh FAHT-toh", "english": "we did/have done", "example": "Abbiamo fatto una passeggiata.", "example_english": "We took a walk."},
            "voi": {"conjugation": "avete fatto", "pronunciation": "ah-VEH-teh FAHT-toh", "english": "you did/have done", "example": "Avete fatto tutto?", "example_english": "Did you do everything?"},
            "loro": {"conjugation": "hanno fatto", "pronunciation": "AHN-noh FAHT-toh", "english": "they did/have done", "example": "Hanno fatto tardi.", "example_english": "They were late."}
        },
        "past_participle": {"form": "fatto", "pronunciation": "FAHT-toh", "english": "done/made"}
    },

    "dare": {
        "infinitive": "dare",
        "infinitive_pronunciation": "DAH-reh",
        "english": "to give",
        "regular": False,
        "auxiliary": "avere",
        "present_tense": {
            "io": {"conjugation": "do", "pronunciation": "doh", "english": "I give", "example": "Io do un regalo.", "example_english": "I give a gift."},
            "tu": {"conjugation": "dai", "pronunciation": "DAH-ee", "english": "you give", "example": "Tu dai una mano?", "example_english": "Do you give a hand?"},
            "lui_lei": {"conjugation": "dà", "pronunciation": "dah", "english": "he/she/it gives", "example": "Lei dà lezioni.", "example_english": "She gives lessons."},
            "noi": {"conjugation": "diamo", "pronunciation": "dee-AH-moh", "english": "we give", "example": "Noi diamo aiuto.", "example_english": "We give help."},
            "voi": {"conjugation": "date", "pronunciation": "DAH-teh", "english": "you give", "example": "Voi date l'esempio.", "example_english": "You set an example."},
            "loro": {"conjugation": "danno", "pronunciation": "DAHN-noh", "english": "they give", "example": "Loro danno consigli.", "example_english": "They give advice."}
        },
        "future_tense": {
            "io": {"conjugation": "darò", "pronunciation": "dah-ROH", "english": "I will give", "example": "Ti darò una risposta.", "example_english": "I will give you an answer."},
            "tu": {"conjugation": "darai", "pronunciation": "dah-RAH-ee", "english": "you will give", "example": "Tu darai il meglio.", "example_english": "You will give your best."},
            "lui_lei": {"conjugation": "darà", "pronunciation": "dah-RAH", "english": "he/she/it will give", "example": "Lei darà una festa.", "example_english": "She will give a party."},
            "noi": {"conjugation": "daremo", "pronunciation": "dah-REH-moh", "english": "we will give", "example": "Daremo una mano.", "example_english": "We will give a hand."},
            "voi": {"conjugation": "darete", "pronunciation": "dah-REH-teh", "english": "you will give", "example": "Voi darete il vostro meglio.", "example_english": "You will give your best."},
            "loro": {"conjugation": "daranno", "pronunciation": "dah-RAHN-noh", "english": "they will give", "example": "Loro daranno tutto.", "example_english": "They will give everything."}
        },
        "past_tense": {
            "io": {"conjugation": "ho dato", "pronunciation": "oh DAH-toh", "english": "I gave/have given", "example": "Ho dato una risposta.", "example_english": "I gave an answer."},
            "tu": {"conjugation": "hai dato", "pronunciation": "AH-ee DAH-toh", "english": "you gave/have given", "example": "Hai dato una mano.", "example_english": "You gave a hand."},
            "lui_lei": {"conjugation": "ha dato", "pronunciation": "ah DAH-toh", "english": "he/she/it gave/has given", "example": "Lei ha dato l'esempio.", "example_english": "She set an example."},
            "noi": {"conjugation": "abbiamo dato", "pronunciation": "ahb-bee-AH-moh DAH-toh", "english": "we gave/have given", "example": "Abbiamo dato tutto.", "example_english": "We gave everything."},
            "voi": {"conjugation": "avete dato", "pronunciation": "ah-VEH-teh DAH-toh", "english": "you gave/have given", "example": "Avete dato il meglio.", "example_english": "You gave your best."},
            "loro": {"conjugation": "hanno dato", "pronunciation": "AHN-noh DAH-toh", "english": "they gave/have given", "example": "Hanno dato consigli.", "example_english": "They gave advice."}
        },
        "past_participle": {"form": "dato", "pronunciation": "DAH-toh", "english": "given"}
    }
}

def complete_irregular_verb(verb_name):
    """Complete an irregular verb JSON file"""
    if verb_name not in irregular_verbs_data:
        print(f"No data for {verb_name}")
        return

    filename = f"VerbData/individual_verbs/{verb_name}.json"
    verb_data = irregular_verbs_data[verb_name]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(verb_data, f, indent=2, ensure_ascii=False)

    print(f"Completed: {filename}")

def main():
    print("Completing irregular verbs with full conjugation data...")

    # Complete the major irregular verbs
    for verb in ["andare", "fare", "dare"]:
        complete_irregular_verb(verb)

if __name__ == "__main__":
    main()