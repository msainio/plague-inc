from flask import Flask, render_template, request

# i (ines) just copied all the imports from the relevance-ranked search engine, we probably don't need all of them
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
from bs4 import BeautifulSoup

#Initialize Flask instance
app = Flask(__name__)

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

    # create a list of dictionaries where {'article': xxx, 'content': yyy} as per the miau1 example
for i,j in zip(name_list, content_list):
    list.append(dict({"article": i, "innehåll": j, "ranked value": ''}))

#Function search() is associated with the address base URL + "/search"
@app.route('/search')

def search():
    matches = []
    search_query = request.args.get('query')


    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(content_list).T.tocsr()
    if search_query:
        query_vec = gv.transform([ search_query ]).tocsc()
        hits = np.dot(query_vec, g_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            for x in range(len(list)):
                if content_list[doc_idx] in list[x]['innehåll']:
                    list[x]['ranked value'] += str(score)
                    matches.append('{}'.format(list[x]))
        print(len(matches))
        print(matches[0])

    #Render index.html with matches variable
    return render_template('plague.html', matches=matches)

