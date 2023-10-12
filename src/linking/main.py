from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import requests
import re


# ========================СОБИРАЕМ ДАННЫЕ===================
with open("src/page_links.txt", "r", encoding="UTF-8") as links_file:
    links_array = links_file.readlines()
with open("src/services_names.txt", "r", encoding="UTF-8") as services_file:
    services_array = services_file.readlines()
with open("src/services_links.txt", "r", encoding="UTF-8") as serv_link_file:
    services_links_arr = serv_link_file.readlines()

services_array = list(map(lambda x: x.replace("\n", ""),
                      services_array))  # Чистим от отступов

services_links_dict = {}

for i in range(len(services_links_arr)):
    services_links_dict[services_array[i]] = services_links_arr[i]


# Намечаем форматирование
block_len = 50
header = "<head>\
    <title>Результаты парсинга</title>\
    <link rel='preconnect' href='https://fonts.googleapis.com'>\
    <link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>\
    <link href='https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap' rel='stylesheet'>\
    <style>\
        div {\
            margin-top: 160px;\
        }\
        body {\
            font-family: 'Roboto', sans-serif;\
            color: black;\
        }\
        body :first-child{\
            margin-top: 0px;\
        }\
        a {\
            color: rgb(52, 181, 255); \
            font-weight:500;\
        }\
        .h3_border { \
            border-top: 1px solid grey\
        }\
        div {\
            text-align: center;\
        }\
        li {\
            margin-bottom: 5px\
        }\
        p {\
            margin-left: 25px\
        }\
    </style>\
</head>"
# обнуляем файл
with open("results/result.html", "w", encoding="UTF-8") as result_file:
    result_file.writelines(header)

# ======================НАЧАЛО ПРОГРАММЫ======================
for url in links_array:
    print("Обрабатываю:", url)
    # Определяем header для файла

    body_header = f"<div><h2>РЕЗУЛЬТАТ ПАРСИНГА</h2><h3>Ссылка : <a target='_blank' href='{url}'>{url}</a></h3></div>"
    # Запрос без авторизации
    responce = requests.get(url, verify=False)

    if responce.status_code == 200:
        bs = BeautifulSoup(responce.text, "html.parser")

        # Подставить сюда классы, по которым делать поиск
        parced_data_els = bs.find_all(
            True, {"class": ["programs__text"]})

        # Объединяем строку
        united_string = ""
        for el in parced_data_els:
            united_string = united_string + el.text.strip().replace("\n", " ")
        # Дробим по всем символам
        united_string = re.split(r'[\W][\s]', united_string)
        
        # Словарь для хранения совпадений
        match_dict = {}
        
        # Находим совпадения
        for part_string in united_string:
            for service in services_array:
                ratio = fuzz.WRatio(part_string.lower(), service.lower())
                if ratio >= 88:
                    if part_string in match_dict:
                        match_dict[part_string].append(service)
                    else:
                        match_dict[part_string] = [service]
        # Оформляем результат
        result_string = ''
        for element in match_dict:
            # Шапка элемента
            result_string = result_string + \
                f"<h3 class='h3_border'>Элемент</h3><p>{element}</p>"

            # Шапка совпадений
            result_string = result_string + "<h3>Совпадения по ключам</h3><ol>"
            for key in match_dict[element]:
                result_string = result_string + \
                    f"<li>{key} | <a>{services_links_dict[key]}</a></li>"  
            result_string = result_string + f"</ol>"

    else:
        result_string = f"Ошибка: {responce.status_code}\n"

    # =========================Заполнение файла============================
    with open("results/result.html", "a", encoding="UTF-8") as result_file:
        result_file.writelines(body_header)
        result_file.writelines(result_string)
