from razdel import tokenize, sentenize
from navec import Navec
from slovnet import Syntax
# from ipymarkup import show_dep_ascii_markup as show_markup  # используется для построения синтаксического дерева

navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
syntax = Syntax.load('slovnet_syntax_news_v1.tar')
syntax.navec(navec)
# Обучаем объект syntax распознавать синтаксические связи на корпусе новостных текстов

# Возвращаем список синтаксических зависимостей для всех токенов во всех предложениях текста
def get_UDs(text):
    result = []
    # Разбиваем текст на предложения и получаем список токенов
    for sentence in sentenize(text):
        tokens = [_.text for _ in tokenize(sentence.text)]
        result.append(tokens)

    dep_res = []
    # Распознаем синтаксические связи с помощью полученных токенов
    for markup in syntax.map(result):
        words = []
        dependencies = []
        # Добавляем слово в список слов, синтаксические зависимости в список зависимостей
        # Раcсчитываем source и target для каждого токена для построения дерева
        for token in markup.tokens:
            words.append(token.text)
            source = int(token.head_id) - 1
            target = int(token.id) - 1
            if source > 0 and source != target:
                dependencies.append([source, target, token.rel])
        # show_markup(words, dependencies)  # Построение дерева
        dep_res.append(dependencies)
    return dep_res

# Подсчитываем безличные и остальные предложения в тексте
def impersonal_sentences(text):
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
    result = {
        'Personal sentences' : personal,
        'Impersonal sentences' : impersonal
    }
    return result

# Подсчитываем простые предложения, различные типы сложных предложений в тексте
def compound_complex(text):
    compound_sent = 0  # сложные предложения
    true_compound = 0  # сложносочиненные предложения
    complex_sent = 0  # сложноподчиненные предложения
    simple_sent = 0  # "простые" предложения, фактически - все остальные
    for sentence in text:
        # Получаем список всех синтаксических зависимостей
        tags = [token[2] for token in sentence]
        if 'mark' in tags:
            complex_sent += 1
        elif 'cc' in tags and 'conj' in tags:
            true_compound += 1
        elif 'cc' not in tags and 'conj' in tags:
            compound_sent += 1
        else:
            simple_sent += 1
    result = {
        'True compound sentences' : true_compound,
        'Complex sentences' : complex_sent,
        'Compound sentences' : compound_sent,
        'Simple sentences': simple_sent
    }
    return result

# Подсчитываем предложения с вводными конструкциями и без них
def introductory_words(text):
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
    result = {
        'Sentences with introductory words' : sent_with_intr_words,
        'Sentences without introductory words' : sent_without_intr_words
    }
    return result
