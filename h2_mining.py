import requests
import re

from bs4 import BeautifulSoup
link = "https://www.helsinginuutiset.fi"
html = requests.get(link).text
soup = BeautifulSoup(html, "html.parser")

headlines = soup.find_all('h2',{'class':'card__title'})

for x in range(len(headlines)):
    print(headlines[x].text)
    print()

