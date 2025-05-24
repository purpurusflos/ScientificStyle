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
# Указываем путь к директории (худ. тексты)
prose_directory ='C:/Workspace/MyPyCharmProjects/ScientificStyle/Prose'

# Находим на сайте Вестника НГУ ссылки на pdf-файлы с научными статьями с 2007 до указанного года
for link in pdf_url_from_vestnik(2008):  # Для 2007 и 2008 годов все работает
    # По ссылке на pdf-файл скачиваем файл в указанную папку
    pdf_from_link(link, directory)

# Получаем список файлов
files = os.listdir(directory)
prose_files = os.listdir(prose_directory)

# Инициализация структуры для результатов
results = {
        'text': [], 'nouns': [],
        '%neut': [], '%femn': [], '%masc': [],
        '%sing': [], '%plur': [], 'verbs': [],
        '%verb(pres)': [], '%verb(past)': [], '%verb(fut)': [],
        'nouns/verbs':[]
        }

results_syntax = {
    'text': [],
    'personal': [],
    'impersonal': [],

    'compound': [],
    'true_compound': [],
    'complex': [],
    'simple': [],

    'sent with intr words': [],
    'sent without intr words': [],

    'participal phrase': [],
    'adverb phrase': [],
    'no phrases': []
    }

results_index = {
        'text': [],
        'average sentence length': [],
        'average number of syllables': [],
        'index': []
        }

def get_result_grammar(
        neut: float, femn: float, masc: float, nouns: float,
        sg: float, pl: float, pres: float, past: float, future: float, verbs: float,
        file: str):
    results['text'].append(file)
    results['nouns'].append(nouns)

    results['%neut'].append(round(100 / nouns * neut if nouns > 0 else 0, 2))
    results['%femn'].append(round(100 / nouns * femn if nouns > 0 else 0, 2))
    results['%masc'].append(round(100 / nouns * masc if nouns > 0 else 0, 2))
    results['%sing'].append(round(100 / nouns * sg if nouns > 0 else 0, 2))
    results['%plur'].append(round(100 / nouns * pl if nouns > 0 else 0, 2))
    results['verbs'].append(verbs)

    results['%verb(pres)'].append(round(100 / verbs * pres if verbs > 0 else 0, 2))
    results['%verb(past)'].append(round(100 / verbs * past if verbs > 0 else 0, 2))
    results['%verb(fut)'].append(round(100 / verbs * future if verbs > 0 else 0, 2))
    results['nouns/verbs'].append(round(nouns / verbs, 2))

def get_result_syntax(
            file: str, personal: float, impersonal: float, compound_sent: float, true_compound: float,
            complex_sent: float, simple_sent: float,
            sent_with_intr_words: float, sent_without_intr_words: float,
        participal_phrase: float, adverb_phrase: float, no_phrases: float):
    results_syntax['text'].append(file)
    total = personal + impersonal
    results_syntax['personal'].append(round(100 / total * personal if total > 0 else 0, 2))
    results_syntax['impersonal'].append(round(100 / total * impersonal if total > 0 else 0, 2))
    results_syntax['compound'].append(round(100 / total * (compound_sent + true_compound + complex_sent) if total > 0 else 0, 2))
    results_syntax['true_compound'].append(round(100 / total * true_compound if total > 0 else 0, 2))
    results_syntax['complex'].append(round(100 / total * complex_sent if total > 0 else 0, 2))
    results_syntax['simple'].append(round(100 / total * simple_sent if total > 0 else 0, 2))

    results_syntax['sent with intr words'].append(round(100 / total * sent_with_intr_words if total > 0 else 0, 2))
    results_syntax['sent without intr words'].append(round(100 / total * sent_without_intr_words if total > 0 else 0, 2))
    results_syntax['participal phrase'].append(round(100 / total * participal_phrase if total > 0 else 0, 2))
    results_syntax['adverb phrase'].append(round(100 / total * adverb_phrase if total > 0 else 0, 2))
    results_syntax['no phrases'].append(round(100 / total * no_phrases if total > 0 else 0, 2))

def get_result_index(average_sentence_length: float, average_number_of_syllables: float, index: float, file: str):
    results_index['text'].append(file)
    results_index['average sentence length'].append(round(average_sentence_length, 2))
    results_index['average number of syllables'].append(round(average_number_of_syllables, 2))
    results_index['index'].append(round(index, 2))

average = ["a621a129b1a4dcd408f350808286f081.pdf",
           "ee9e6f31d702584e354a81ffa8547ef2.pdf",
           "232605f541d931e034b6271963bf52d3.pdf",
           "9eecf541a6d5c79a0d043ed546326679.pdf",
           "dbfd8e46c680a0562021664689beccd6.pdf",
           "bc59e553aafa67549c9e42f61f573383.pdf",
           "df1315441c3f2f5b3c6de9aae2067e55.pdf",
           "de41992d630662c2a9ed66584af3f7ce.pdf",
           "dd3813413f41b24b70428223eebefa22.pdf",
           "016798dea64580a1b8503dd60efbaf5c.pdf"]

# Получаем статистику для первых 10 файлов (можно изменить)
for num, file_name in enumerate(average):
    # Открываем файл в бинарном режиме только для чтения
    with open(directory + '/' + file_name, 'rb') as file:
        # Извлекаем текст в виде строки из pdf-файла
        text = get_text(file)
        # Убираем цитирования и при необходимости восстанавливаем постановку пробелов
        text1 = re.sub(r"\s\[.*?]", "", text)
        clear_text = re.sub(r"([а-я\)])([\.\?\!]{1})([А-Я])", r"\1\2 \3", text1)
    # Для каждого слова в каждом предложении получаем слова с UD-разметкой
    text_UD = get_UDs(clear_text)

    neut, femn, masc, nouns, sg, pl, pres, past, future, verbs = get_grammar(text)
    get_result_grammar(neut, femn, masc, nouns, sg, pl, pres, past, future, verbs, "scientific text " + str(num + 1))

    personal, impersonal = impersonal_sentences(text_UD)
    true_compound, complex_sent, compound_sent, simple_sent = compound_complex(text_UD)
    sent_with_intr_words, sent_without_intr_words = introductory_words(text_UD)
    participal_phrase, adverb_phrase, no_phrases = participal_phrases(text_UD)
    get_result_syntax(
        "scientific text " + str(num + 1), personal, impersonal,
        compound_sent, true_compound, complex_sent, simple_sent,
        sent_with_intr_words, sent_without_intr_words, participal_phrase, adverb_phrase, no_phrases)

    average_sentence_length, average_number_of_syllables, index = readability(clear_text)
    get_result_index(average_sentence_length, average_number_of_syllables, index, "scientific text " + str(num + 1))

# Художественные тексты
for num, file_name in enumerate(prose_files[:10]):
    # Открываем файл в бинарном режиме только для чтения
    with open(prose_directory + '/' + file_name, encoding='utf-8') as file:
        # Извлекаем текст в виде строки из pdf-файла
        text = file.read()
        text_UD = get_UDs(text)

        neut, femn, masc, nouns, sg, pl, pres, past, future, verbs = get_grammar(text)
        get_result_grammar(neut, femn, masc, nouns, sg, pl, pres, past, future, verbs, "prose text " + str(num + 1))

        personal, impersonal = impersonal_sentences(text_UD)
        true_compound, complex_sent, compound_sent, simple_sent = compound_complex(text_UD)
        sent_with_intr_words, sent_without_intr_words = introductory_words(text_UD)
        participal_phrase, adverb_phrase, no_phrases = participal_phrases(text_UD)
        get_result_syntax(
            "prose text " + str(num + 1), personal, impersonal,
            compound_sent, true_compound, complex_sent, simple_sent,
            sent_with_intr_words, sent_without_intr_words, participal_phrase, adverb_phrase, no_phrases)

        average_sentence_length, average_number_of_syllables, index = readability(text)
        get_result_index(average_sentence_length, average_number_of_syllables, index, "prose text " + str(num + 1))


grammar_gender = pd.DataFrame({
        'text': results['text'],
        'neutral, %': results['%neut'],
        'feminine, %': results['%femn'],
        'masculine, %': results['%masc'],
        })

grammar_number = pd.DataFrame({
        'text': results['text'],
        'singular, %': results['%sing'],
        'plural, %': results['%plur'],
        })

grammar_verbs = pd.DataFrame({
        'text': results['text'],
        'present, %': results['%verb(pres)'],
        'past, %': results['%verb(past)'],
        'future, %': results['%verb(fut)']
        })

grammar_POS = pd.DataFrame({
        'text': results['text'],
        'nouns': results['nouns'],
        'verbs': results['verbs'],
        'nouns/verbs': results['nouns/verbs']
        })

syntax_impersonal = pd.DataFrame({
        'text': results_syntax['text'],
        'personal, %': results_syntax['personal'],
        'impersonal, %': results_syntax['impersonal']
        })

syntax_simple_compound = pd.DataFrame({
        'text': results_syntax['text'],
        'compound, %': results_syntax['compound'],
        'simple, %': results_syntax['simple'],
        })

syntax_compound_complex = pd.DataFrame({
        'text': results_syntax['text'],
        'compound, %': results_syntax['true_compound'],
        'complex, %': results_syntax['complex']
        })

syntax_introductory_words = pd.DataFrame({
        'text': results_syntax['text'],
        'Introductory words, %': results_syntax['sent with intr words'],
        'No introductory words, %': results_syntax['sent without intr words'],
        })

syntax_participal_phrases = pd.DataFrame({
        'text': results_syntax['text'],
        'Participal phrases, %': results_syntax['participal phrase'],
        'Adverb phrases, %': results_syntax['adverb phrase'],
        'No phrases, %': results_syntax['no phrases'],
        })

index = pd.DataFrame({
        'text': results_index['text'],
        'av. sent. length': results_index['average sentence length'],
        'av. num. of syllables': results_index['average number of syllables'],
        'index': results_index['index'],
        })

# Таблицы
print(grammar_gender)
print(grammar_number)
print(grammar_verbs)
print(grammar_POS)
print(syntax_impersonal)
print(syntax_simple_compound)
print(syntax_compound_complex)
print(syntax_introductory_words)
print(syntax_participal_phrases)
print(index)
