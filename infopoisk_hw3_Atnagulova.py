from math import log
from collections import defaultdict
import requests
import re
from pymystem3 import Mystem
import os
from flask import Flask
from flask import render_template, request

def collection(folder, stop):
    m = Mystem()
    data = {}
    data_lemmas = []
    for root, dirs, files in os.walk(folder):
        for fname in files:
            f = open(root + '/' + fname, 'r', encoding = 'utf-8')
            article = f.read()
            f.close()
            article += '.'
            title = re.findall('@ti (.*?)\n', article)[0]
            url = re.findall('@url (.*?)\n', article)[0]
            text = re.findall('@url.*?\n(.*)\.', article, flags = re.DOTALL)[0]
            data[title] = [url, text]
        
    for key in data:
        wo_stop = []
        data[key][1] = re.sub('\n', ' ', data[key][1])
        data[key][1] = re.sub(' – ', ' ', data[key][1])
        data[key][1] = re.sub('[.,!?:;\'\"\(\)\[\]«»]', '', data[key][1])
        while '  ' in data[key][1]:
            data[key][1] = re.sub('  ', ' ', data[key][1])
        all_words = data[key][1].split(' ')
        dl = len(all_words)
        lemmas = m.lemmatize(data[key][1])
        for lem in lemmas:
            if lem not in stop:
                wo_stop.append(lem)
        data_lemmas.append([key, data[key][0], wo_stop, dl, all_words])
    
    return data_lemmas, data
            
def search_req(message, stop):
    message_lemmas = []
    m = Mystem()
    lemmas = m.lemmatize(message)
    for lem in lemmas:
        if lem not in stop:
            message_lemmas.append(lem)
    
    return message_lemmas

def actual_rev_index(data):
    ind = defaultdict(list)
    for article in data:
        for word in article[2]:
            if data.index(article) not in ind[word]:
                ind[word].append(data.index(article))
    return ind

def AVDL(corp_lemm, read_collection):
    length_all_art = 0
    for art in corp_lemm:
        length_all_art += art[3]
    avdl = length_all_art / len(read_collection)
    return avdl

def ranking(message_lemmas, corp_lemm, reverse_ind, read_collection):
    fits = {}
    N = len(corp_lemm)
    avdl = AVDL(corp_lemm, read_collection)
    out = {}
    counter = 0
    for message_word in message_lemmas:
        if message_word in reverse_ind:
            in_articles = reverse_ind[message_word]
            fits[message_word] = in_articles
            
    for mess_word in fits:
        n = len(fits[mess_word])
        for article in fits[mess_word]:
            actual_article_data = corp_lemm[article]
            dl = actual_article_data[3]
            full_text = corp_lemm[article][4]
            occurrences = 0
            for word in full_text:
                if word == mess_word:
                    occurrences += 1
            fq = occurrences/dl
            score = score_BM25(n, fq, N, dl, avdl)
            out[counter] = [corp_lemm[article][0], score, corp_lemm[article][1], mess_word]
            counter += 1
    return out

def output(out):
    titles = []
    for article in sorted(out, key=lambda n: out[n][1], reverse=True)[:10]:
        if len(titles) == 0:
            titles.append((out[article][0], out[article][2]))
        else:
            for title in titles:
                if out[article][0] not in title[0]:
                    titles.append((out[article][0],out[article][2]))
    return titles

def score_BM25(n, fq, N, dl, avdl):
    k1 = 2.0
    b = 0.75
    K = compute_K(dl, avdl)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * fq) / (K + fq)
    return IDF * frac

def compute_K(dl, avdl):
    k1 = 2.0
    b = 0.75
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))

app = Flask(__name__)

@app.route('/', methods=['get', 'post'])
def my_search():
    stop = [' ', '\n', 'бы', 'быть', 'в', 'за', 'его', 'ее', 'весь', 'вот', 'все', 'всей', 'вы', 'говорить', 'да', 'для', 'до', 'еще', 'же', 'знать', 'и', 'из', 'к', 'как', 'который', 'мочь', 'мы', 'на', 'наш', 'не', 'него', 'нее', 'нет', 'них', 'но', 'о', 'один', 'она', 'они', 'оно', 'оный', 'от', 'ото', 'по', 'с', 'свой', 'себя', 'сказать', 'та', 'такой', 'только', 'тот', 'ты', 'у', 'что', 'это', 'этот', 'я']
    if request.form:
       full_word = request.form['phrase']
       if full_word:
           corp_lemm, read_collection = collection('Corpora', stop)
           message_lemmas = search_req(full_word, stop)
           out = ranking(message_lemmas, corp_lemm, actual_rev_index(corp_lemm), read_collection)
           titles = output(out)
       return render_template('my_search.html', titles=titles)
    return render_template('my_search.html')

if __name__ == '__main__':
    app.run()
