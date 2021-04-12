# use links from battle_links_spider to gather battle info, write to json
import requests
from bs4 import BeautifulSoup
import json
import wikipedia

wikiURL = 'https://wikipedia.org/wiki/'
battleArray = []

with open('./battlesLinks.json') as f:
    data = json.load(f)

for i in data:
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
    summary = wikipedia.summary(i)
    summary = summary.replace("–", "-")

    infobox = soup.select('.infobox')[0].find_all('td')
    if infobox[1].select("img"):
        print("image layout..")

        # date
        # print(infobox[3].get_text())
        date = infobox[3].get_text()

        # location
        # print(infobox[4].select("div.location")[0].get_text())
        location = infobox[4].select("div.location")[0].get_text()

        # image
        image = ''
        if soup.select('.infobox')[0].findAll('img'):
            images = soup.select('.infobox')[0].findAll('img')
            # print(images[0]['src'])
            image = images[0]['src']
        else:
            print("no image found")

        # outcome
        # print(infobox[5].get_text())
        outcome = infobox[5].get_text()

        # flags side a
        flags_array = []
        if(infobox[6].select("span.flagicon")):
            flags = infobox[6].select("span.flagicon")
            flag_count = len(flags)
            print(flag_count)
            i = 0

            while i < flag_count:
                flag_image = flags[i].findAll("img")
                flags_array.append(flag_image[0]["src"])
                i += 1
            print(flags_array)

        # belligerents
        # print(infobox[3].get_text())
        # MAKE THESE ARRAYS AND ADD EACH <a> tag as one item
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

        date = date.replace("–", "-")
        date = date.replace("&nbsp;", " ")
        location = location.replace("\ufeff", "x")
        location = location.replace("\u2032", "'")
        location = location.replace("&nbsp;", " ")

        # make the JSON
        # battle = {
        #     "title": title,
        #     "date": date,
        #     "summary": summary,
        #     "side_a": side_a_array,
        #     "side_b": side_b_array,
        #     "location": location,
        #     "image_url": image,
        #     "outcome": outcome,
        #     "flags": flags_array,
        #     "url": battleLink
        # }

        # print(json.dumps(battle, indent=4, sort_keys=True))

        # battleArray.append(battle)


# with open('battle.json', 'w') as f:
#     json.dump(battleArray, f, indent=4, ensure_ascii=False, sort_keys=True)

    # else:
    #     print("no-image layout..")

    # if soup.select('.infobox')[0].findAll('img'):
    #     print('imaged article..')
    #     infobox = soup.select('.infobox')[0].find_all('td')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # with open('battles.json', 'w') as f:
    #     json.dump(array, f, indent=4, ensure_ascii=False)

    # loop through each battle page, grab stuff i want, save to JSON
    # else:
    #     print('no image!..')
