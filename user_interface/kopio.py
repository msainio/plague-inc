

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer 
import math
import numpy as np 
import requests 
import re
from bs4 import BeautifulSoup
import ipdb

url = "../data/enwiki-1000-corpus.txt"

content_list = []
name_list = []
list = []

document = open(url, "r")
corpus = document.read().replace('\n', ' ')
document.close()
soup = BeautifulSoup(corpus, "html.parser")
for article in soup.find_all('article'):
    content_list.append(article.contents.pop())
    name_list.append(article.get('name'))

for i,j in zip(name_list, content_list):
    list.append({"article": i, "content": j, "ranked value": '0'})


def search():
    matches = []
#    query = str(input("what is your query? "))
    query = "hej"

    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(content_list).T.tocsr()
    if query:
        query_vec = gv.transform([ query ]).tocsc()
        hits = np.dot(query_vec, g_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            for x in range(len(list)):
                if content_list[doc_idx] in list[x]['content']:
                    list[x]['ranked value'] += str(score)
                    #print(list[x])
                    matches.append(list[x])


    ids = []
    scores = []
    for i in matches:
        ids.append(i['article'])
        scores.append(i['ranked value'])
#    print(ids)
#    print(scores)

    print(hits[0])
search()
