from pdf_from_nsu_vestnik import pdf_url_from_vestnik
from pdf_from_nsu_vestnik import pdf_from_link
from text_from_pdf import get_text
from syntax_from_sentence import get_UDs
from syntax_from_sentence import impersonal_sentences
from syntax_from_sentence import compound_complex
from syntax_from_sentence import introductory_words
import os

text1 = 'В полной  мере  их  значение  лидеры  антибольшевистского  движения  осознали  лишь  под  «занавес» своей борьбы. Они явно опасались заимствовать  у  большевиков  их  опыт,  оправдавший себя  в  условиях  гражданской  войны.  Намного быстрее,  к  концу  1918 г.,  обозначилось  стремление  в  условиях  инфляции  и  товарного  дефицита  в  процессе  повышения  заработной  платы сглаживать  различия  в  материальной  оценке разных категорий служащих. Сходство с тем, что происходило  в  условиях  советской  власти,  очевидно, хотя это не осознавалось лидерами контрреволюции.'
text2 = "В саду, замечу, растут цветы, напоминающие бабочек. Ваня, по мнению ученых, решает задачи, мама моет раму. Сегодня, безусловно, очень жарко."

# Находим на сайте Вестника НГУ ссылки на pdf-файлы с научными статьями с 2007 до указанного года
for link in pdf_url_from_vestnik(2008):  # Для 2007 и 2008 годов все работает
    # По ссылке на pdf-файл скачиваем файл
    pdf_from_link(link)
    print("Articles are downloaded")

# Указываем путь к директории
directory = "C:/Workspace/MyPyCharmProjects/ScientificStyle/Articles"
# Получаем список файлов
files = os.listdir(directory)
print("Files are got")

for file_name in files:
    # print(file_name)  # чтобы понять, в каком файле проблема
    # Открываем файл в бинарном режиме только для чтения
    with open(directory + '/' + file_name, 'rb') as file:
        # Извлекаем текст в виде строки из pdf-файла
        text = get_text(file)
        # print(text[:1000])  # чтобы понять, если текст считался неверно
    if text == "":
        print("ALERT ALERT THERE'S NO TEXT")  # чтобы узнать, когда текст не считался совсем
    else:
        # Для каждого слова в каждом предложении получаем слова с UD-разметкой
        text_UD = get_UDs(text)
        # Выводим результат
        print(impersonal_sentences(text_UD), compound_complex(text_UD), introductory_words(text_UD))
