import requests
from bs4 import BeautifulSoup
import json

with open('./WikiData/battlesAll/allbattles.json', encoding="utf8") as f:
    data = json.load(f)

battle_edits = []
count = 0

for i in data:

    title = i["battleLabel"]
    date = i["point_in_time"]
    war = i["part_ofLabel"]
    coords = i["coordinate_location"]
    link = i["battle"]

    coords2 = coords.replace('Point(', '')
    coords3 = coords2.replace(')', '')
    coords4 = coords3.split(' ')

    coords4[0], coords4[1] = coords4[1], coords4[0]

    new_battle = {
        "title": title,
        "war": war,
        "date": date,
        "latitude": coords4[0],
        "longitude": coords4[1],
        "link": link
    }
    battle_edits.append(new_battle)
    count = count + 1
    print(count)

with open('WikiData/battlesAll/parser/edits.json', 'w') as f:
    json.dump(battle_edits, f, indent=4, ensure_ascii=True, sort_keys=False)
