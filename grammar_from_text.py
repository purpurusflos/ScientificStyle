import pymorphy3
import re

morph = pymorphy3.MorphAnalyzer()

def get_grammar(text):
    # Делим текст на слова
    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text)
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
    return neut, femn, masc, nouns, sg, pl, pres, past, future, verbs
