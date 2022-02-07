# This is the code for the search engine task. First we import modules we need for this.
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
from bs4 import BeautifulSoup

# Here we define the dataset for the search engine
url = "enwiki-corpus.txt"

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

# These functions are used by the boolean search function to parse the query entered by the user

def rewrite_token(t, d):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query, d):
    return " ".join(rewrite_token(t, d) for t in query.split())

# This function executes a boolean query and displays the results

def bool_query(query):
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w+\b") # token pattern set to one alphanumeric
    sparse_matrix = cv.fit_transform(corpus_list)
    sparse_td_matrix = sparse_matrix.T.tocsr()
    t2i = cv.vocabulary_

    d = {"and": "&", "AND": "&",
         "or": "|", "OR": "|",
         "not": "1 -", "NOT": "1 -",
         "(": "(", ")": ")"}

    hits_matrix = eval(rewrite_query(query, d))
    hits_list = list(hits_matrix.nonzero()[1])

    print("Found {} matching documents.".format(len(hits_list)))
    if len(hits_list) > 0:
        num_matches = int(input("Please enter the maximum amount of matches to be displayed: "))
        print()
        for i, doc_idx in enumerate(hits_list):
            if i > (num_matches-1): # limits the amount of matches displayed
                break
            print("Match {:d}: {:10s} -> {:s}".format(i+1, name_list[doc_idx], corpus_list[doc_idx][:99])) # sets the amount of characters to be displayed
        print()
    else:
        pass



def ranked_query(query):
    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(corpus_list).T.tocsr()

    # Vectorize query string
    query_vec = gv.transform([ query ]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, g_matrix)

    # Rank hits
    try:
        ranked_scores_and_doc_ids = \
            sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                   reverse=True)

    # Output result
        print("Your query '{:s}' matches the following documents:".format(query))
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            print("Match {:d}: (score: {:.4f}): {:s}".format(i+1, score, name_list[doc_idx]))
        print()
    except:
        print("Found {} matching documents.".format(0))
        print()

# This is the main program.
def main():
    print("Welcome to the Plague Engine!")

    consent = str(input("Do you want to go on an epic quest for astounding knowledge (y/n)? "))

    while consent != "n":
        print()
        print("Would you like to perform a Boolean search or a Relevance-Ranked search?")

        search_type = str(input("Please enter 'b' for Boolean or 'r' for Relevance-Ranked: "))
        while search_type not in ["b", "r"]:
            print("Invalid option entered.")
            search_type = str(input("Please enter 'b' for Boolean or 'r' for Relevance-Ranked: "))
        print()

        if search_type == "b":
            print("Search type: Boolean")
        else:
            print("Search type: Relevance-Ranked")

        search_query = str(input("Please type your query here: "))
        print()

        if search_type == "b":
            bool_query(search_query)
        else:
            ranked_query(search_query)

        consent = str(input("Do you want to go on another epic quest for astounding knowledge (y/n)? "))

    print("Goodbye!")

main()
