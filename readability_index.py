from razdel import tokenize, sentenize
from navec import Navec
from slovnet import Syntax


navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
syntax = Syntax.load('slovnet_syntax_news_v1.tar')
syntax.navec(navec)
# Обучаем объект syntax распознавать синтаксические связи на корпусе новостных текстов

# Рассчитываем среднюю длину предложения в словах
def ave_length(sentences):
    words_count = 0
    sentences_count = len(sentences)
    for s in sentences:
        # Считаем слова по количеству пробелов
        words_count += s.count(" ") + 1
    return words_count / sentences_count

# Рассчитываем среднюю длину слов в слогах
def ave_syllable(sent_tokens):
    syllables_count = 0
    words = []
    for markup in syntax.map(sent_tokens):
        for token in markup.tokens:
            # Проверяем, что токен не является знаком препинания
            if token.rel != "punct":
                words.append(token)
                # Считаем количество слогов, то есть гласных букв в слове
                for vowel in "УЕЫАОЭЯИЮЁёуеаоэяиюы":
                    syllables_count += token.text.count(vowel)
    return syllables_count / len(words)

# Считаем индекс читабельности
def readability(text):
    sentences = []
    sent_tokens = []
    # Разбиваем текст на предложения и получаем список токенов
    for sentence in sentenize(text):
        tokens = [_.text for _ in tokenize(sentence.text)]
        sent_tokens.append(tokens)
        sentences.append(sentence.text)
    # Считаем индекс читабельности для русского языка по формуле Флеша
    # 206,836 – (1,52 × средняя длина предложения) – (65,14 × среднее число слогов)
    index = 206.836 - (1.52 * ave_length(sentences)) - (65.14 * ave_syllable(sent_tokens))
    return index
