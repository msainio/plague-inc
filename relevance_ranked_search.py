# This is the code for the search engine task
from sklearn.feature_extraction.text import CountVectorizer
import math

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

#    document = open(url, "r")
#    corpus = document.read().replace('\n', ' ').replace('>', '')
#    document.close()
#    corpus_list = corpus.split("</article")

except FileNotFoundError:
    print("One or more of the input documents was not found.")

# Here we transform the dataset into a matrix

cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w+\b") # token pattern set to one alphanumeric
sparse_matrix = cv.fit_transform(corpus_list)
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_

# Here we define the search operators

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

# These functions parse the query entered by the user

def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query):
    return " ".join(rewrite_token(t) for t in query.split())

# This function executes the query and displays the results

def init_query(query):
    try:
        print(query)
        hits_matrix = eval(rewrite_query(query))
        hits_list = list(hits_matrix.nonzero()[1])
        print()
        if len(hits_list) == 0:
            raise ValueError
        print("Found {} matching documents.".format(len(hits_list)))
        num_matches = int(input("Please enter the maximum amount of matches to be displayed: "))
        print()
        for i, doc_idx in enumerate(hits_list):
            if i > (num_matches-1): # limits the amount of matches displayed
                break
            print("Match {:d}: {:10s} -> {:s}".format(i+1, name_list[doc_idx], corpus_list[doc_idx][15:114])) # sets the amount of characters to be displayed
        print()
    except:
        print("No match found. Please enter another query.")
        print()

def init_relquery(rquery):
    print("hi")

# This is the main program.

def main():
    print("Welcome to the Plague Engine!")
    print("You can search our database by submitting a query in the input field below.")
    print("To exit the program, enter an empty string when prompted.")
    print()
    # Asking the user which type of a search they want to perform
    searchtype = str(input("Would you like to perform a Boolean search or a Relevance-Ranked search? Enter B for Boolean and R for Relevance-Ranked. "))
    if searchtype == "B":
        query = str(input("Please type your query here: "))
        while query != "":
            init_query(query)
            query = str(input("Please type your query here: "))
        print("No query entered. Program terminated.")
        exit()
    elif searchtype == "R":
        rquery = str(input("Please type your query here: "))
        while rquery != "":
             init_relquery(rquery)
             query = str(input("Please type your query here: "))
        print("No query entered. Program terminated.")
        exit()
    else:
        print("Invalid option entered. Program terminated.")
        exit()

main()
