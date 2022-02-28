# Imports useful modules
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Initializes the Flask instance
app = Flask(__name__)

url = "data/enwiki-1000-corpus.txt"

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

# Creates a list of dictionaries of the form {'article': xxx, 'content': yyy}
for i,j in zip(name_list, content_list):
    list.append(dict({"article": i, "contents": j, "ranked value": '', 'hits in document': ''}))

# Assigns the search function to an address composed of the base URL and "/search"
@app.route('/search')

def search():
    matches = []
    scores = []
    search_query = request.args.get('query')

    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(content_list).T.tocsr()
    if search_query:
        query_vec = gv.transform([ search_query ]).tocsc()
        hits = np.dot(query_vec, g_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            for x in range(len(list)):
                if content_list[doc_idx] in list[x]['contents']:
                    list[x]['ranked value'] += str(score)
                    matches.append(list[x])

        fig = plt.figure()
        for i in matches:
            scores.append(float(i['ranked value']))
        if len(scores) > 20:
            scores = scores[:20]
        ranks = []
        for i in range(1,(len(scores)+1)):
            ranks.append(str(i))
        plt.bar(ranks, scores)
        fig.savefig('static/bar_graph.png', dpi=200)

# Renders the HTML file and imports the variable 'matches'
    return render_template('plague.html', matches=matches)
