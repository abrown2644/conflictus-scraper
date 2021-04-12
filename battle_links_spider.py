# grab links of all battles for use in battle_spider
import requests
from bs4 import BeautifulSoup
import json

response = requests.get(
    'https://en.wikipedia.org/wiki/List_of_battles_(alphabetical)')

soup = BeautifulSoup(response.content, 'html.parser')

array = []
subStrings = ['/wiki/Battle', '/wiki/Operation', 'wiki/Attack',
              'wiki/Seige', 'wiki/Fall', 'wiki/First', 'wiki/Second', 'wiki/Warsaw']

for link in soup.find_all('a'):
    strLink = str(link.get('href'))
    if any(x in strLink for x in subStrings):
        array.append(strLink)

with open('battles.json', 'w') as f:
    json.dump(array, f, indent=4, ensure_ascii=False)
