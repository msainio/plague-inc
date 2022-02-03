import requests
import re
from bs4 import BeautifulSoup

corpus_list = []
name_list = []

document = open("enwiki-corpus.txt", "r")
corpus = document.read().replace('\n', ' ')
soup = BeautifulSoup(corpus, "html.parser")
for article in soup.find_all('article'):
    corpus_list.append(article.contents.pop())
    name_list.append(article.get('name'))
document.close()

for x in range(len(corpus_list)):
    print("article nr.{:3d}: '{}': {}".format(x, name_list[x], corpus_list[x][:99]))
