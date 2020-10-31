import re

# step 1 templates
RVRE = re.compile(r'^(.*?[аеиоуыэюя])(.*)$')
PERFECTIVEGROUND = re.compile(r'((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$')
REFLEXIVE = re.compile(r'(с[яь])$')
ADJECTIVE = re.compile(r'(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$')
VERB = re.compile(r'((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить'
                  r'|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$')
NOUN = re.compile(r'(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию'
                  r'|ью|ю|ия|ья|я)$')
I = re.compile(r'и$')
PARTICIPLE = re.compile(r'((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$')
DERIVATIONAL = re.compile(r'(ость|ост)$')
P = re.compile(r'ь$')
NN = re.compile(r'нн$')
SUPERLATIVE = re.compile(r'(ейше|ейш)$')
NOT_LETTER = re.compile(r'[^a-яА-Яё]$')

string = ''
word = ''
path_to_text = ''

def input_data():
    global word, path_to_text, string
    word = input("Введите слово: " + "\n").lower()
    path_to_text = input("Введите путь к файлу (по умолчанию 'D:\Учёба\\7 семестр -\- Технологии обработки информации (Экз)\Лабораторная работа №2\Testing text.txt')" + "\n")


def get_text():
    while True:
        try:
            global path_to_text, string
            file = open(path_to_text, "r")

            for line in file:
                string += line
            file.close()
            break

        except:
            path_to_text = input("Не найден указанный путь. Попробуйте еще раз, или введите 'NO', чтобы завершить: " + "\n")
            if path_to_text.upper() == "NO":
                break


def stemming(word):
    word = word.lower()
    word = word.replace('ё', 'e')
    area = re.match(RVRE, word)

    if area is not None:
        PREFIX = area.group(1)
        RV = area.group(2)
        # point
        print(area.group(1))

        # step 1
        template = PERFECTIVEGROUND.sub('', RV, 1)
        if template == RV:
            RV = REFLEXIVE.sub('', RV, 1)
            template = ADJECTIVE.sub('', RV, 1)

            if template != RV:
                RV = template
                RV = PARTICIPLE.sub('', RV, 1)
            else:
                template = VERB.sub('', RV, 1)
                if template == RV:
                    RV = NOUN.sub('', RV, 1)
                else:
                    RV = template
        else:
            RV = template

        # step 2
        RV = I.sub('', RV, 1)

        # step 3
        RV = DERIVATIONAL.sub('', RV, 1)

        # step 4
        template = NN.sub('н', RV, 1)
        if template == RV:
            template = SUPERLATIVE.sub('', RV, 1)
            if template != RV:
                RV = template
                RV = NN.sub('н', RV, 1)
            else:
                RV = P.sub('', RV, 1)
        else:
            RV = template
        word = PREFIX + RV
    return word


def match_search(base_of_word, string):
    result = []
    text = string.replace('\n', ' ').split(' ')                     # массив слов обработанных
    print(text)
    for word in text:
        word = NOT_LETTER.sub('', word, 1)                          # топор
        word = word.lower()
        temp = '^' + base_of_word
        flag = re.match(temp, word)
        print(word)
        # if base_of_word in word:
        if flag:
            result.append(word)
    return result


input_data()
get_text()
base_of_word = stemming(word)
result_words = match_search(base_of_word, string)
if len(result_words) == 0:
    print("Слов с одиннаковой основой не обнаружено")
else:
    # print("Совпадения по основанию слова: ")
    f = open('result.txt', 'w')
    for word in result_words:
        f.write(word + '\n')
    f.close()
