import re
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def get_grammar(words):
    nouns = verbs = 0
    neutral = feminine = masculine = 0
    singular = plural = 0
    present = past = future = 0
    for word in words:
        parsed = morph.parse(word)[0]
        tag = parsed.tag
        part_of_speech = str(tag.POS)
        gender = str(tag.gender)
        number = str(tag.number)
        tense = str(tag.tense)

        if part_of_speech == 'NOUN':
            nouns += 1
            if gender == 'neut':
                neutral += 1
            elif gender == 'femn':
                feminine += 1
            elif gender == 'masc':
                masculine += 1

            if number == 'sing':
                singular += 1
            elif number == 'plur':
                plural += 1

        elif part_of_speech == 'VERB':
            verbs += 1
            if tense == 'pres':
                present += 1
            elif tense == 'past':
                past += 1
            elif tense == 'futr':
                future += 1
    return nouns, verbs, neutral, feminine, masculine, singular, plural, present, past, future

def process_morphology(file_name, text):
    # Инициализация структуры для результатов
    results = {
        'text': [], 'nouns': [], 'neut': [], '%neut': [],
        'femn': [], '%femn': [], 'masc': [], '%masc': [],
        'sing': [], 'plur': [], 'verbs': [],
        '%verb(pres)': [], '%verb(past)': [], '%verb(fut)': []
    }

    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text)
    nouns, verbs, neutral, feminine, masculine, singular, plural, present, \
        past, future = get_grammar(words)

    results['text'].append(file_name[:-4])
    results['nouns'].append(nouns)

    results['neut'].append(neutral)
    results['%neut'].append(round(100 / nouns * neutral if nouns > 0 else 0, 2))
    results['femn'].append(feminine)
    results['%femn'].append(round(100 / nouns * feminine if nouns > 0 else 0, 2))
    results['masc'].append(masculine)
    results['%masc'].append(round(100 / nouns * masculine if nouns > 0 else 0, 2))

    results['sing'].append(singular)
    results['plur'].append(plural)

    results['verbs'].append(verbs)

    results['%verb(pres)'].append(round(100 / verbs * present if verbs > 0 else 0, 2))
    results['%verb(past)'].append(round(100 / verbs * past if verbs > 0 else 0, 2))
    results['%verb(fut)'].append(round(100 / verbs * future if verbs > 0 else 0, 2))

    return results