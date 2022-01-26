import requests
import re

from bs4 import BeautifulSoup
link = "https://www.hs.fi"
html = requests.get(link).text
soup = BeautifulSoup(html, "html.parser")

#for tag in soup.find_all(re.compile("h2")):
#    print(tag)

headlines = soup.find_all('h2',{'class':'teaser-title-40'})
for i in range(len(headlines)):
    print(headlines[i].text)
headlines_2 = soup.find_all('h2',{'class':'teaser-title-30'})
for i in range(len(headlines_2)):
    print(headlines_2[i].text)
