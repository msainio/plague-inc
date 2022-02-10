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

url = "../../data/enwiki-1000-corpus.txt"

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

except FileNotFoundError:
    print("One or more of the input documents was not found.")

# create a list of dictionaries where {'article': xxx, 'content': yyy} as per the miau1 example
for i,j in zip(name_list, corpus_list):
    list.append({'article': i, 'content': j})


#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        #Look at each entry in the example data
        for entry in list:
            #If an entry name contains the query, add the entry to matches
            if query.lower() in entry['article'].lower():
                matches.append(entry)

    #Render index.html with matches variable
    return render_template('plague.html', matches=matches)
