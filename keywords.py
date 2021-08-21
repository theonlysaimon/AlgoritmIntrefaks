from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
from collections import Counter
import np
import json
from pymystem3 import Mystem
from nltk import FreqDist
import string
import os 
import re
    
#загрузка dataset
with open("data/dataset_public.json", "r", encoding="utf8") as read_file:
    ng_1_data = json.load(read_file)

with open ('data/stop_ru.txt', 'r', encoding="utf8") as stop_file:
    rus_stops = [word.strip() for word in stop_file.readlines()] 

extended_punctuation = string.punctuation + '—»«...'
moi_analizator = Mystem()

def passed_filter (some_word, stoplist):
    some_word = some_word.strip()
    if some_word in extended_punctuation:
        return False
    elif some_word in stoplist:
        return False
    elif re.search ('[А-ЯЁа-яёA-Za-z]', some_word) == None:
        return False
    return True

def keywords_most_frequent_with_stop_and_lemm (some_text, num_most_freq, stoplist):
    lemmatized_text = [word for word in moi_analizator.lemmatize(some_text.lower()) 
                       if passed_filter(word, stoplist)]
    return [word_freq_pair[0] for word_freq_pair in FreqDist(lemmatized_text).most_common(num_most_freq)]

def preprocess_for_tfidif (some_text):
    lemmatized_text = moi_analizator.lemmatize(some_text.lower())
    return (' '.join(lemmatized_text)) # поскольку tfidf векторайзер принимает на вход строку

def produce_tf_idf_keywords (some_texts, number_of_words):
    make_tf_idf = TfidfVectorizer (stop_words=rus_stops)
    texts_as_tfidf_vectors=make_tf_idf.fit_transform(preprocess_for_tfidif(text) for text in some_texts)
    id2word = {i:word for i,word in enumerate(make_tf_idf.get_feature_names())} 

    for text_row in range(texts_as_tfidf_vectors.shape[0]): 
        # берем ряд в нашей матрице -- он соответстует тексту:
        row_data = texts_as_tfidf_vectors.getrow(text_row)
        # сортируем в нем все слова: 
        words_for_this_text = row_data.toarray().argsort() 
        # берем число слов с конца, равное number_of_words 
        top_words_for_this_text = words_for_this_text [0, :-1*(number_of_words+1):-1]
        # возращаем результат
        return [id2word[w] for w in top_words_for_this_text]

manual_keywords = [] ## сюда запишем все ключевые слова, приписанные вручную
full_texts = [] ## сюда тексты

for item in ng_1_data:
    manual_keywords.append(item['title'])
    full_texts.append(item['news'][1]['body'])

#вывод результатов на экран
print ('Эталонные ключевые слова: ', manual_keywords [:1])
print ('Самые частотные слова: ', produce_tf_idf_keywords(full_texts[:1], 6))
