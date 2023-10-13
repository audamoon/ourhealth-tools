from gseleniumconf.chrome import ChromeConfigurator
from sheethelper.manager import SheetManager
import json 

driver = ChromeConfigurator.get_driver()
gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs")

EMAIL_RANGE = "B:B"
BUSINESS_URL_RANGE = "E:E"
RESULT_RANGE = "N:N"
FIRST_DATA_LETTER = "H"
LAST_DATA_LETTER = "M"

with open ("collect/data/Sites.json", "r", encoding="UTF-8") as sites_json:
    sites_data = json.load(sites_json)

urls = gs.reader.read_range(BUSINESS_URL_RANGE)

for site in sites_data["sites"]:
    row_ids = gs.reader.find_row_id_by_two_word(EMAIL_RANGE, RESULT_RANGE, site["email"], "НЕТ")
    for row_id in row_ids:
        url = urls[row_id - 1][0]
        table_data = gs.reader.read_range(f"{FIRST_DATA_LETTER}{row_id}:{LAST_DATA_LETTER}{row_id}")[0]
        numbers = table_data[:2]
        socials = table_data[2:]
