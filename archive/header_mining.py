import requests
import re

from bs4 import BeautifulSoup
link = "https://www.helsinginuutiset.fi"
html = requests.get(link).text
soup = BeautifulSoup(html, "html.parser")

headlines = soup.find_all('h2',{'class':'card__title'})

print("Below are the results of our mining: News headlines extracted from helsinginuutiset.fi")
print("")
for x in range(len(headlines)):
    print(headlines[x].text)
    print()

