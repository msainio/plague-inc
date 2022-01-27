

import requests
import re

from bs4 import BeautifulSoup
document = open("enwiki-corpus.txt", "r")
soup = BeautifulSoup(document, "html.parser")

#headlines = soup.find_all('h2',{'class':'card__title'})

document.close()

articles = soup.article['name']

for x in range(len(articles)):
    print(articles[x].text)
    print()
#article = soup.article['name']

#article = soup.find_all('article')
print(article)
