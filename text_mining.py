from bs4 import BeautifulSoup
url = "hs.fi"
html = urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
