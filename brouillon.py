import json

f = json.loads(open("data/items.json", "r").read())
print(len(list(f.keys())))