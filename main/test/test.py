import json

with open("test.json","r",encoding="UTF-8") as file:
    a = json.load(file)
for el in a["string_array"]:
    print(el["string_name"])
    