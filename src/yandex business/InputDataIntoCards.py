from gseleniumconf.chrome import ChromeConfigurator 
from sheethelper.manager import SheetManager
from modules.BusinessCard import BusinessCard
import json 
import time


LOGIN_RANGE = "B:B"
RESULT_RANGE = "N:N"
BUSINESS_URL_RANGE = "E:E"
FIRST_DATA_LETTER = "H"
LAST_DATA_LETTER = "M"

driver = ChromeConfigurator.get_driver()
gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs")

with open ("json/login.json", "r", encoding="UTF-8") as sites_json:
    login = json.load(sites_json)["login"]

row_ids = gs.reader.find_row_id_by_two_word(LOGIN_RANGE, RESULT_RANGE, login, "НЕТ")

if (len(row_ids) == 0):
    exit("Нечего проверять")

urls = gs.reader.read_range(BUSINESS_URL_RANGE)

for row_id in row_ids:
    url = urls[row_id - 1][0]
    table_data = gs.reader.read_range(f"{FIRST_DATA_LETTER}{row_id}:{LAST_DATA_LETTER}{row_id}")[0]
    numbers = table_data[:2]
    socials = table_data[2:]
    driver.get(url.replace("/main", ""))
    
    card = BusinessCard(driver, socials, numbers)
    card.compare_values()
    time.sleep(100)