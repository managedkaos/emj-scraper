from bs4 import BeautifulSoup
import requests


resp = requests.get("https://www.tandfonline.com/toc/uemj20/32/1")
html = resp.text

soup = BeautifulSoup(html, features="html.parser")
spans = soup.find_all('span', {'class' : 'hlFld-Title'})

lines = [span.get_text() for span in spans]

print(lines)
