import json
with open("test/text_test.json","r",encoding="utf-8") as f:
    a = json.load(f)
for key in a:
    print(f"h1 = {key}")
    for el in a[key]:
        for key2 in el:
            if key2 == "h2":
                print(el[key2])