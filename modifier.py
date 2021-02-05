import json
import requests
from random import randint
from sys import argv

items = json.loads(open("data/items.json", "r", encoding="utf-8").read())

for item_key in list(items.keys())[:]:
    try:
        target = items[item_key]["image"]
        print(target)
        img = requests.get(target, allow_redirects=True, verify=False)
        if target[-3:-1] == "jpg":
            save = open(f"C:/Users/hyoug/code/python/pcc/ressources/{item_key}.jpg", "wb")
        else:
            save = open(f"C:/Users/hyoug/code/python/pcc/ressources/{item_key}.png", "wb")
        save.write(img.content)
        save.close()

        print(f"Le fichier {item_key} a été sauvegardé sous le nom : {item_key}.png "
              f"[{list(items.keys()).index(item_key)}/{len(items.keys())}]")

    except requests.exceptions.MissingSchema:
        print(f"Echec {item_key} : {items[item_key]['image']}"
              f"[{list(items.keys()).index(item_key) + 1}/{len(items.keys())}]")



