import requests
import re

from bs4 import BeautifulSoup
link = "https://www.hs.fi"
html = requests.get(link).text
soup = BeautifulSoup(html, "html.parser")

for tag in soup.find_all(re.compile("h2")):
    print(tag)
