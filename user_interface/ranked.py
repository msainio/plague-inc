# This is the code for the search engine task. First we import modules we need for this.
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
from bs4 import BeautifulSoup

# Here we define the dataset for the search engine

url = "../data/enwiki-1000-corpus.txt"

corpus_list = []
name_list = []

try:
    document = open(url, "r")
    corpus = document.read().replace('\n', ' ')
    document.close()
    soup = BeautifulSoup(corpus, "html.parser")
    for article in soup.find_all('article'):
        corpus_list.append(article.contents.pop())
        name_list.append(article.get('name'))

except FileNotFoundError:
    print("One or more of the input documents was not found.")


def ranked_query(query):
    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(corpus_list).T.tocsr()

    # Vectorize query string
    query_vec = gv.transform([ query ]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, g_matrix)

    # Rank hits
    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

    # Output result
#        print("Found {} matching documents.".format(len(ranked_scores_and_doc_ids)))
#        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
#            if i > (num_matches-1):
#                break
#            print("Match {:d}: (score: {:.4f}): {:s}".format(i+1, score, name_list[doc_idx]))
#    except:
#        print("An error occurred.")

# This is the main program.
def main():
    search_query = "yes"
    while search_query != "":
        search_query = str(input("What is your query? "))
        ranked_query(search_query)
    exit()

main()

