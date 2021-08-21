import json
from pymystem3 import Mystem
import string
import os 

while exit:
#загрузка dataset
    while True:
        try:
            print("Введите путь к файлу:    ")
            path = input()        
            path = path.replace('\\','/')
            
            with open(path, "r", encoding="utf8") as read_file:
                ng_1_data = json.load(read_file)
            break
        except ValueError:
            print("Ошибка значения")
        except IOError:
            print("Файл не найден")

    with open ("C:/Users/Monst/Documents/GitHub/AlgoritmIntrefaks/data/stop_ru.txt", 'r', encoding="utf8") as stop_file:
        rus_stops = [word.strip() for word in stop_file.readlines()] 

    extended_punctuation = string.punctuation + '—»«...'
    moi_analizator = Mystem()

    def passed_filter (some_word, stoplist):
        import re
        some_word = some_word.strip()
        if some_word in extended_punctuation:
            return False
        elif some_word in stoplist:
            return False
        elif re.search ('[А-ЯЁа-яёA-Za-z]', some_word) == None:
            return False
        return True

    def keywords_most_frequent_with_stop_and_lemm (some_text, num_most_freq, stoplist):
        from nltk import FreqDist
        lemmatized_text = [word for word in moi_analizator.lemmatize(some_text.lower()) 
                        if passed_filter(word, stoplist)]
        return [word_freq_pair[0] for word_freq_pair in FreqDist(lemmatized_text).most_common(num_most_freq)]

    while True:
        try:
            print("Введите количество прогоняемых кластеров:    ")

            clast = int(input())
            for item in ng_1_data[:clast]:
                print ('Эталонные ключевые слова: ', item['title'])
                print ('Самые частотные слова: ',  keywords_most_frequent_with_stop_and_lemm (item['news'][1]['body'], 6, rus_stops))
                print ("")
            break
        except ValueError:
            print("Неверное значение")  

    print("Работа завершена")
    while True:
        try:
            print("Желаете продолжить? y/n")
            exitpool = input()
            if exitpool == 'n':
                exit = False
            elif exitpool == 'y':
                exit = True
                break
        except ValueError:
            print("Введите y или n")