import requests
import re

from bs4 import BeautifulSoup
document = open("enwiki-corpus.txt", "r")
soup = BeautifulSoup(document, "html.parser")
corpus = document.read()
article = corpus.split("</article>")
#headlines = soup.find_all('h2',{'class':'card__title'})

document.close()

list_of_articles = []

for x in soup.find_all('article'):
    list_of_articles.append((x.get('name')))

print(list_of_articles)


#namelist.append(name)
#print(x.get('name'))
#articles = soup.article['name']
#x = soup.find_all('</article>')
#for x in range(len(articles)):
#    print(articles[x].text)
#    print()
#article = soup.article['name']

#article = soup.find_all('article')
#print(articles)
#print(article)
