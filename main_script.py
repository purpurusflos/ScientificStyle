from pdf_from_nsu_vestnik import pdf_url_from_vestnik
from pdf_from_nsu_vestnik import pdf_from_link
from text_from_pdf import get_text
from morphology_analysis import process_morphology
from syntax_from_sentence import get_UDs
from syntax_from_sentence import impersonal_sentences
from syntax_from_sentence import compound_complex
from syntax_from_sentence import introductory_words
from syntax_from_sentence import participal_phrases
from readability_index import readability
import os
import re

# Указываем путь к директории
directory = "C:/Workspace/MyPyCharmProjects/ScientificStyle/Articles"

# # Находим на сайте Вестника НГУ ссылки на pdf-файлы с научными статьями с 2007 до указанного года
# for link in pdf_url_from_vestnik(2008):  # Для 2007 и 2008 годов все работает
#     # По ссылке на pdf-файл скачиваем файл в указанную папку
#     pdf_from_link(link, directory)

# Получаем список файлов
files = os.listdir(directory)

for file_name in files:
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
        print(process_morphology(file_name, clear_text))
        print(readability(clear_text), impersonal_sentences(text_UD), compound_complex(text_UD), introductory_words(text_UD), participal_phrases(text_UD))
