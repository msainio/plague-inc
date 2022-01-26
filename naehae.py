from urllib import request
from bs4 import BeautifulSoup

url = "http://www.hs.fi"
html = request.urlopen(url).read().decode('utf8')
soup = BeautifulSoup(html, 'html.parser')

print(soup.find_all('span'))
