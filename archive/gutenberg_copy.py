from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import nltk

url = "enwiki-corpus.txt"

corpus_list = []
name_list = []

document = open(url, "r")
corpus = document.read().replace('\n', ' ')
document.close()
soup = BeautifulSoup(corpus, "html.parser")
for article in soup.find_all('article'):
    corpus_list.append(article.contents.pop())
    name_list.append(article.get('name'))

    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(corpus_list).T.tocsr()

    # Vectorize query string
    query_vec = gv.transform([ query_string ]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, g_matrix)

    # Rank hits
    ranked_scores_and_doc_ids = \
        sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
               reverse=True)

    # Output result
    print("Your query '{:s}' matches the following documents:".format(query_string))
    for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
        print("Doc #{:d} (score: {:.4f}): {:s}".format(i, score, name_list[doc_idx]))
    print()


search_gutenberg("hero")
