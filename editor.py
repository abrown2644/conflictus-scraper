import json

# file = open('./battlesV2/battle_v2.json')
# battles = json.load(file)
# count = 0
# print(battles)

# for item in battles:
#     item.id = count
#     count += 1
#     print(item.title)

# with open('battles_with_ids.json', 'w') as f:
#     json.dump(battles, f, indent=4, sort_keys=True)

count = 0
with open('./battlesV2/battle_v2.json') as json_file:
    data = json.load(json_file)
    print(data)
#     for item in data:
#         item['id'] = count
#         count += 1
#         print(item['title'])

# with open('battles_with_ids.json', 'w') as f:
#     json.dump(data, f, indent=4, sort_keys=True)
