
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

    templates.append({
        'name': f'Infinitive - En->It',
        'qfmt': f'{{{{English}}}}',
        'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{Infinitive}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>'})
    templates.append({
         'name': f'Infinitive - It->En',
         'qfmt': f'{{{{Infinitive}}}}',
         'afmt': f'{{{{FrontSide}}}}<hr id="answer">{{{{English}}}}<br><br><b>Infinitive:</b> {{{{Infinitive}}}}<br><b>{{{{Reflexive}}}}</b><br><b><div class={regular_tag}>{{{{Regular}}}}</div></b>',})

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