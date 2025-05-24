from razdel import tokenize, sentenize
from navec import Navec
from slovnet import Syntax

# Обучаем объект syntax распознавать синтаксические связи на корпусе новостных текстов.
navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
syntax = Syntax.load('slovnet_syntax_news_v1.tar')
syntax.navec(navec)


# Возвращаем список синтаксических зависимостей для всех токенов во всех предложениях текста.
def get_UDs(text: str) -> list:
    result = []
    # Разбиваем текст на предложения и получаем список токенов.
    for sentence in sentenize(text):
        tokens = [_.text for _ in tokenize(sentence.text)]
        result.append(tokens)

    dep_res = []
    # Распознаем синтаксические связи с помощью полученных токенов.
    for markup in syntax.map(result):
        dependencies = []
        # Добавляем синтаксические зависимости в список зависимостей.
        # Раcсчитываем source и target для каждого токена.
        for token in markup.tokens:
            source = int(token.head_id) - 1
            target = int(token.id) - 1
            if source > 0 and source != target:
                dependencies.append([source, target, token.rel])
        dep_res.append(dependencies)
    # Возвращает список, где каждое предложение - отдельный список с токенами.
    return dep_res


# Подсчитываем безличные и остальные предложения в тексте.
def impersonal_sentences(text: list) -> tuple:
    personal = 0
    impersonal = 0
    for sentence in text:
        # Получаем список всех синтаксических зависимостей
        tags = [token[2] for token in sentence]
        # Проверяем, есть ли в предложении именное подлежащее
        if 'nsubj' in tags or 'nsubj:pass' in tags or 'nsubj:outer' in tags:
            personal += 1
        else:
            impersonal += 1
    # Возвращает целые числа: число небезличных предложений и число безличных предложений.
    return personal, impersonal


# Подсчитываем простые предложения, различные типы сложных предложений в тексте
def compound_complex(text: list) -> tuple:
    compound_sent = 0  # сложные предложения
    true_compound = 0  # сложносочиненные предложения
    complex_sent = 0  # сложноподчиненные предложения
    simple_sent = 0  # "простые" предложения, фактически - все остальные
    for sentence in text:
        # Получаем список всех синтаксических зависимостей
        tags = [token[2] for token in sentence]
        # Проверяем наличие в предложении подчинительных союзов.
        if 'mark' in tags:
            complex_sent += 1
        elif 'cc' in tags and 'conj' in tags:
            true_compound += 1
        elif 'cc' not in tags and 'conj' in tags:
            compound_sent += 1
        else:
            simple_sent += 1
    # Возвращает целые числа: количество сложных предложений, сложносочиненных предложений,
    # сложноподчиненных и простых предложений.
    return true_compound, complex_sent, compound_sent, simple_sent


# Подсчитываем предложения с вводными конструкциями и без них.
def introductory_words(text: list) -> tuple:
    sent_with_intr_words = 0
    sent_without_intr_words = 0
    for sentence in text:
        # Получаем список всех синтаксических зависимостей
        tags = [token[2] for token in sentence]
        # Проверяем, есть ли в предложении вводная конструкция
        if 'parataxis' in tags:
            sent_with_intr_words += 1
        else:
            sent_without_intr_words += 1
    # Возвращает целые числа: количество предложений с вводными словами и без них.
    return sent_with_intr_words, sent_without_intr_words


# Подсчитываем предложения с причастными и деепричастными оборотами и без них.
def participal_phrases(text: list) -> tuple:
    participal_phrase = 0
    adverb_phrase = 0
    no_phrases = 0
    for sentence in text:
        # Получаем список всех синтаксических зависимостей
        tags = [token[2] for token in sentence]
        # Проверяем, есть ли в предложении причастные и деепричастные обороты
        if 'advcl' in tags:
            adverb_phrase += 1
        if 'amod' in tags:
            participal_phrase += 1
        if 'advcl' not in tags and 'amod' not in tags:
            no_phrases += 1
    # Возвращает целые числа: количество предложений с причастными и деепричастными оборотами и без них.
    return participal_phrase, adverb_phrase, no_phrases
