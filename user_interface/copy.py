from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
from bs4 import BeautifulSoup

url = "../data/enwiki-1000-corpus.txt"

corpus_list = []
name_list = []
list = []

try:
    document = open(url, "r")
    corpus = document.read().replace('\n', ' ')
    document.close()
    soup = BeautifulSoup(corpus, "html.parser")
    for article in soup.find_all('article'):
        corpus_list.append(article.contents.pop())
        name_list.append(article.get('name'))

    # create a list of dictionaries where {'article': xxx, 'content': yyy} as per the miau1 example
    for i,j in zip(name_list, corpus_list):
        list.append({"article": i, "content": j})
except:
    pass


def search():
    matches = []
    query = 'hero'


    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(corpus_list).T.tocsr()
    if query:
        query_vec = gv.transform([ query ]).tocsc()
        hits = np.dot(query_vec, g_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        for x, (score, id) in enumerate(ranked_scores_and_doc_ids):
            matches.append(entry)
    print(matches)

    #Render index.html with matches variable
    #return render_template('plague.html', matches=matches)
