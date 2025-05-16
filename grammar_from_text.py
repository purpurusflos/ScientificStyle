import pymorphy2
import re

def get_grammar(text):
    # Делим текст на слова
    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text)
    morph = pymorphy2.MorphAnalyzer()
    neut = femn = masc = nouns = sg = pl = pres = past = future = verbs = 0

    for word in words:
        # получаем часть речи для слова
        tag = morph.parse(word)[0].tag
        pos = str(tag.POS); gender = str(tag.gender); num = str(tag.number); tense = str(tag.tense)
        if pos == 'NOUN':
            nouns += 1
            if gender == 'neut':
                neut += 1
            elif gender == 'femn':
                femn += 1
            elif gender == 'masc':
                masc += 1
            if num == 'sing':
                sg += 1
            elif num == 'plur':
                pl += 1
        elif pos == 'VERB':
            verbs += 1
            if tense == 'pres':
                pres += 1
            elif tense == 'past':
                past += 1
            elif tense == 'futr':
                future += 1
    result = {
        'nouns': nouns, 'neut': neut, '%neut': round(100 / nouns * neut if nouns > 0 else 0, 2),
        'femn': femn, '%femn': round(100 / nouns * femn if nouns > 0 else 0, 2), 'masc': masc, '%masc': round(100 / nouns * masc if nouns > 0 else 0, 2),
        'sing': sg, 'plur': pl, 'verbs': verbs,
        #'verb(pres)': pres, 'verb(past)': past, 'verb(fut)': futur,
        '%verb(pres)': round(100 / verbs * pres if verbs > 0 else 0, 2), '%verb(past)': round(100 / verbs * past if verbs > 0 else 0, 2), '%verb(fut)': round(100 / verbs * future if verbs > 0 else 0, 2)
    }
    return result
