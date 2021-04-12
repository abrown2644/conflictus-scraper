# use links from battle_links_spider to gather battle info, write to json
import requests
from bs4 import BeautifulSoup
import json
import wikipedia

wikiURL = 'https://wikipedia.org/wiki/'
battleArray = []
no_image_battles = []

with open('./battlesLinks.json') as f:
    data = json.load(f)

for i in data:
    try:
        # print('link: ', wikiURL + i)
        battleLink = wikiURL + i
        print('link: ', battleLink)
        response = requests.get(battleLink)
        soup = BeautifulSoup(response.content, 'html.parser')
        print("~~~ start ~~~~")

        # title
        # print(soup.select('.firstHeading')[0].get_text())
        title = soup.select('.firstHeading')[0].get_text()

        # summary
        # print(wikipedia.summary(i))
        try:
            summary = wikipedia.summary(i)
            summary = summary.replace("–", "-")
        except Exception:
            summary = "no_battle_summary"

        try:
            infobox = soup.select('.infobox')[0].find_all('td')
        except Exception:
            print("exception found on infobox")
            print("**adding to no image battles**")
            no_image_battles.append(battleLink)
            continue

        if infobox[1].select("img"):
            print("image layout..")
            # date
            # print(infobox[3].get_text())
            date = infobox[3].get_text()

            # image
            image = ''
            if soup.select('.infobox')[0].findAll('img'):
                images = soup.select('.infobox')[0].findAll('img')
                # print(images[0]['src'])
                image = images[0]['src']
            else:
                print("no image found")
                image = "no_battle_image"

            # location
            if infobox[4].select("div.location")[0]:
                location = infobox[4].select("div.location")[0].get_text()
            elif infobox[3].select("div.location")[0]:
                location = infobox[3].select("div.location")[0].get_text()
            else:
                location = "no_location"

            # outcome
            # print(infobox[5].get_text())
            outcome = {
                "description": infobox[5].get_text(),
                "winner": "no_battle_winner"
            }

            infobox[5].get_text()

            # belligerents
            side_a_array = []
            side_b_array = []

            side_a = infobox[6].select("a")
            side_b = infobox[7].select("a")

            # print("--side a--")
            for member_a in side_a:
                if(member_a.find("img")):
                    pass
                else:
                    side_a_array.append(member_a.get_text())
            # print(side_a_array)

            # print("--side b--")
            for member_b in side_b:
                if(member_b.find("img")):
                    pass
                else:
                    side_b_array.append(member_b.get_text())
            # print(side_b_array)

            # flags side a
            flags_array_a = []
            if(infobox[6].select("span.flagicon")):
                flags = infobox[6].select("span.flagicon")
                # print(flags)
                flag_count = len(flags)
                # print(flag_count)
                i = 0

                while i < flag_count:
                    flag_image = flags[i].findAll("img")
                    if(flags[i].a):
                        flag_name = flags[i].a["title"]
                    else:
                        flag_name = "no_flag_name"
                    # print(flag_name)
                    flag_object = {
                        "img_url": flag_image[0]["src"],
                        "name": flag_name
                    }
                    flags_array_a.append(flag_object)
                    # flags_array_a.append(flag_image[0]["src"])
                    i += 1
                # print(flags_array_a)

            # flags side b
            flags_array_b = []
            if(infobox[7].select("span.flagicon")):
                flags = infobox[7].select("span.flagicon")
                # print(flags)
                flag_count = len(flags)
                # print(flag_count)
                i = 0

                while i < flag_count:
                    flag_image = flags[i].findAll("img")
                    if(flags[i].a):
                        flag_name = flags[i].a["title"]
                    else:
                        flag_name = "no_flag_name"
                    # print(flag_name)
                    flag_object = {
                        "img_url": flag_image[0]["src"],
                        "name": flag_name
                    }
                    flags_array_b.append(flag_object)
                    i += 1
                # print(flags_array_b)

            # commanders a
            commanders_a = []
            commanders_a_div = infobox[8].select("a")

            for commander in commanders_a_div:
                if commander.get_text():
                    commanders_a.append(commander.get_text())
            # print(commanders_a)

            # commanders b
            commanders_b = []
            commanders_b_div = infobox[9].select("a")

            for commander in commanders_b_div:
                if commander.get_text():
                    commanders_b.append(commander.get_text())
            # print(commanders_b)

            # strength TODO
            strength_a = ["no_battle_strength"]
            strength_b = ["no_battle_strength"]

            # losses TODO
            losses_a = ["no_battle_losses"]
            losses_b = ["no_battle_losses"]

            # make any corrections
            date = date.replace("–", "-")
            date = date.replace("&nbsp;", " ")
            location = location.replace("\ufeff", "x")
            location = location.replace("\u2032", "'")
            location = location.replace("&nbsp;", " ")

            # complete date
            date_obj = {
                "description": date,
                "iso": "no_battle_iso"
            }

            side_a_complete = {
                "participants": side_a_array,
                "flags": flags_array_a,
                "commanders": commanders_a,
                "strength": strength_a,
                "losses": losses_a
            }

            side_b_complete = {
                "participants": side_b_array,
                "flags": flags_array_b,
                "commanders": commanders_b,
                "strength": strength_b,
                "losses": losses_b
            }

            # make the JSON
            battle = {
                "title": title,
                "war": "no_battle_war",
                "date": date_obj,
                "summary": summary,
                "location": location,
                "image_url": image,
                "outcome": outcome,
                "side_a": side_a_complete,
                "side_b": side_b_complete,
                "url": battleLink
            }

            # print(json.dumps(battle, indent=4, sort_keys=True))

            battleArray.append(battle)

        else:
            print("no image layout...")
            print("**adding to no image battles**")
            no_image_battles.append(battleLink)
    except(Exception):
        continue

# Write battles
with open('battle.json', 'w') as f:
    json.dump(battleArray, f, indent=4, ensure_ascii=True, sort_keys=False)

# Write missing image battles
with open('no_image_battles.json', 'w') as f:
    json.dump(no_image_battles, f, indent=4, ensure_ascii=True)
