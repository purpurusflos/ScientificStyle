from razdel import tokenize, sentenize
from navec import Navec
from slovnet import Syntax

# Обучаем объект syntax распознавать синтаксические связи на корпусе новостных текстов.
navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
syntax = Syntax.load('slovnet_syntax_news_v1.tar')
syntax.navec(navec)


# Рассчитываем среднюю длину предложения в словах.
def ave_length(sentences: list) -> float:
    words_count = 0
    sentences_count = len(sentences)
    for s in sentences:
        # Считаем слова по количеству пробелов
        words_count += s.count(" ") + 1
    # Возвращает вещественное число - среднюю длину предложения в словах.
    return words_count / sentences_count


# Рассчитываем среднюю длину слов в слогах.
def ave_syllable(sent_tokens: list) -> float:
    syllables_count = 0
    words = []
    for markup in syntax.map(sent_tokens):
        for token in markup.tokens:
            # Проверяем, что токен не является знаком препинания.
            if token.rel != "punct":
                words.append(token)
                # Считаем количество слогов по количеству гласных букв в слове.
                for vowel in "УЕЫАОЭЯИЮЁёуеаоэяиюы":
                    syllables_count += token.text.count(vowel)
    # Возвращает вещественное число - среднюю длину слова в слогах.
    return syllables_count / len(words)


# Считаем индекс читабельности.
def readability(text: str) -> tuple:
    sentences = []
    sent_tokens = []
    # Разбиваем текст на предложения и получаем список токенов.
    for sentence in sentenize(text):
        tokens = [_.text for _ in tokenize(sentence.text)]
        sent_tokens.append(tokens)
        sentences.append(sentence.text)
    # Считаем индекс читабельности для русского языка по адаптированной формуле Флеша:
    # 206,836 – (1,52 × средняя длина предложения) – (65,14 × среднее число слогов)
    index = 206.836 - (1.52 * ave_length(sentences)) - (65.14 * ave_syllable(sent_tokens))
    # Возвращает вещественные числа: среднюю длину предложения в словах, среднюю длину слов в слогах
    # и индекс читабельности для конкретного текста
    return ave_length(sentences), ave_syllable(sent_tokens), index
