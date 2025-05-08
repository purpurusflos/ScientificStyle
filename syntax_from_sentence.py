from razdel import tokenize, sentenize
from navec import Navec
from slovnet import Syntax
from ipymarkup import show_dep_ascii_markup as show_markup

navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
syntax = Syntax.load('slovnet_syntax_news_v1.tar')
syntax.navec(navec)

text1 = 'В полной  мере  их  значение  лидеры  антибольшевистского  движения  осознали  лишь  под  «занавес» своей борьбы. Они явно опасались заимствовать  у  большевиков  их  опыт,  оправдавший себя  в  условиях  гражданской  войны.  Намного быстрее,  к  концу  1918 г.,  обозначилось  стремление  в  условиях  инфляции  и  товарного  дефицита  в  процессе  повышения  заработной  платы сглаживать  различия  в  материальной  оценке разных категорий служащих. Сходство с тем, что происходило  в  условиях  советской  власти,  очевидно, хотя это не осознавалось лидерами контрреволюции.'

def get_UDs(text):
    result = []
    for sentence in sentenize(text):
        tokens = [_.text for _ in tokenize(sentence.text)]
        result.append(tokens)

    dep_res = []
    for sentence in result:
        markup = next(syntax.map([sentence]))
        words = []
        dependencies = []
        for token in markup.tokens:
            words.append(token.text)
            source = int(token.head_id) - 1
            target = int(token.id) - 1
            if source > 0 and source != target:
                dependencies.append([source, target, token.rel])
        # show_markup(words, dependencies)
        dep_res.append(dependencies)
    return dep_res

a = get_UDs(text1)
print(a)