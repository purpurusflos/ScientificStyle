from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar


def text_extraction(element):
    # Извлекаем текст из вложенного текстового элемента
    line_text = element.get_text()

    # Находим форматы текста
    # инициализируем список со всеми форматами, встречающимися в строке текста
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Обходим каждый символ в строке текста
            for character in text_line:
                if isinstance(character, LTChar):
                    # Добавляем к символу название шрифта
                    line_formats.append(character.fontname)
                    # Добавляем к символу размер шрифта
                    line_formats.append(character.size)
    # Находим уникальные размеры и названия шрифтов в строке
    format_per_line = list(set(line_formats))

    # Возвращаем кортеж с текстом в каждой строке вместе с его форматом
    return line_text, format_per_line

# Очищаем текст от знаков переноса на новую строку и
# объединяем в одну строку
def clean_text(page_content):
    text1 = ""
    text2 = ""
    for text in page_content:
        split_text1 = text.split("-\n")
        clean_text1 = "".join(split_text1)
        text1 += clean_text1
    split_text2 = text1.split("\n")
    clean_text2 = "".join(split_text2)
    text2 += clean_text2
    return text2

def get_text(file_path):
    page_content = []

    for page_number, page in enumerate(extract_pages(file_path)):
        # Находим все элементы
        page_elements = page._objs

        # Находим элементы, составляющие страницу
        for i, element in enumerate(page_elements):
            # Проверяем, является ли элемент текстовым
            if isinstance(element, LTTextContainer):
                # Используем функцию извлечения текста и формата для каждого текстового элемента
                (line_text, format_per_line) = text_extraction(element)
                # print(line_text, format_per_line)

                if 10.019999999999982 in format_per_line or 10.980000000000018 in format_per_line or 11.0 in format_per_line and len(line_text.split()) > 3:
                    page_content.append(line_text)

                if "Список литературы" in line_text:
                    return clean_text(page_content)
    return clean_text(page_content)
