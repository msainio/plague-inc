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

print(list[:2])
