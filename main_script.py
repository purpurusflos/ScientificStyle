from pdf_from_nsu_vestnik import pdf_url_from_vestnik
from pdf_from_nsu_vestnik import pdf_from_link
from text_from_pdf import get_text
from syntax_from_sentence import get_UDs
from syntax_from_sentence import impersonal_sentences
from syntax_from_sentence import compound_complex
from syntax_from_sentence import introductory_words
from syntax_from_sentence import participal_phrases
from readability_index import readability

from grammar_from_text import get_grammar
import pandas as pd

import os
import re

# Указываем путь к директории
directory = "C:/Workspace/MyPyCharmProjects/ScientificStyle/Articles"

# Находим на сайте Вестника НГУ ссылки на pdf-файлы с научными статьями с 2007 до указанного года
for link in pdf_url_from_vestnik(2008):  # Для 2007 и 2008 годов все работает
    # По ссылке на pdf-файл скачиваем файл в указанную папку
    pdf_from_link(link, directory)

# Получаем список файлов
files = os.listdir(directory)

# Инициализация структуры для результатов
results = {
        'text': [], 'nouns': [], '%neut': [],
        #'neut': [],'femn': [], 'masc': [],
        '%femn': [], '%masc': [],
        '%sing': [], '%plur': [], 'verbs': [],
        #'verb(pres)': [], 'verb(past)': [], 'verb(fut)': [],
        '%verb(pres)': [], '%verb(past)': [], '%verb(fut)': []
        }
grammar_nouns = pd.DataFrame({
        'text': results['text'],
        'nouns': results['nouns'],
        #'neut': results['neut'],
        '%neut': results['%neut'],
        #'femn': results['femn'],
        '%femn': results['%femn'],
        #'masc': results['masc'],
        '%masc': results['%masc'],
        '%sing': results['%sing'],
        '%plur': results['%plur']
    })
grammar_verbs = pd.DataFrame({
        'text': results['text'],
        'verbs': results['verbs'],
        #'verb(pres)': results['verb(pres)'],
        '%verb(pres)': results['%verb(pres)'],
        #'verb(past)': results['verb(past)'],
        '%verb(past)': results['%verb(past)'],
        #'verb(fut)': results['verb(fut)'],
        '%verb(fut)': results['%verb(fut)']
        })

def get_result(neut, femn, masc, nouns, sg, pl, pres, past, future, verbs, file):
    results['text'].append(file)
    results['nouns'].append(nouns)
    #results['neut'].append(neut)
    results['%neut'].append(round(100 / nouns * neut if nouns > 0 else 0, 2))
    #results['femn'].append(femn)
    results['%femn'].append(round(100 / nouns * femn if nouns > 0 else 0, 2))
    #results['masc'].append(masc)
    results['%masc'].append(round(100 / nouns * masc if nouns > 0 else 0, 2))
    results['%sing'].append(round(100 / nouns * sg if nouns > 0 else 0, 2))
    results['%plur'].append(round(100 / nouns * pl if nouns > 0 else 0, 2))
    results['verbs'].append(verbs)
    # results['verb(pres)'].append(pres)
    results['%verb(pres)'].append(round(100 / verbs * pres if verbs > 0 else 0, 2))
    # results['verb(past)'].append(past)
    results['%verb(past)'].append(round(100 / verbs * past if verbs > 0 else 0, 2))
    # results['verb(fut)'].append(future)
    results['%verb(fut)'].append(round(100 / verbs * future if verbs > 0 else 0, 2))

# Получаем статистику для первых 10 файлов (можно изменить)
for num, file_name in enumerate(files[:10]):
    # Открываем файл в бинарном режиме только для чтения
    with open(directory + '/' + file_name, 'rb') as file:
        # Извлекаем текст в виде строки из pdf-файла
        text = get_text(file)
        # Убираем цитирования и при необходимости восстанавливаем постановку пробелов
        text1 = re.sub(r"\s\[.*?]", "", text)
        clear_text = re.sub(r"([а-я\)])([\.\?\!]{1})([А-Я])", r"\1\2 \3", text1)
    if clear_text != "":
        # Для каждого слова в каждом предложении получаем слова с UD-разметкой
        text_UD = get_UDs(clear_text)
        # Выводим результат для каждого предложения
        print(readability(clear_text), impersonal_sentences(text_UD), compound_complex(text_UD), introductory_words(text_UD), participal_phrases(text_UD))
        neut, femn, masc, nouns, sg, pl, pres, past, future, verbs = get_grammar(text)
        get_result(neut, femn, masc, nouns, sg, pl, pres, past, future, verbs, "scientific text " + str(num))

print(grammar_nouns)
print(grammar_verbs)
