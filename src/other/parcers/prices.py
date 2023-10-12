import requests
import bs4
import json

res = requests.get("https://triumf.center/tseny/")
print(res.text)
soup = bs4.BeautifulSoup(res.text,"html.parser")

names = soup.find_all(class_="price__table-subtitle")
prices = soup.find_all(class_="price__table-price")


to_json = {}

for i in range (len(names)):
    to_json[f"price-{i}"] = [names[i].text.replace("                                    ","").replace("\r\n"," "),prices[i].text.replace("\r\n","")]

with open("prices.json","w", encoding="UTF-8") as f:
    json.dump(to_json,f,ensure_ascii=False)