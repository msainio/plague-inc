import requests
from bs4 import BeautifulSoup
link = "https://www.hs.fi"
html = requests.get(link).text
soup = BeautifulSoup(html, "html.parser")
print(soup.get_text())
