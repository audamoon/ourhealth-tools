from gseleniumconf.chrome import ChromeConfigurator
from sheethelper.manager import SheetManager
from modules.SiteCollector import SiteCollector
import json

driver = ChromeConfigurator.get_driver()
gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs")

LOGIN_RANGE = "B:B"
URL_RANGE = "G:G"

with open ("json/sites.json", "r", encoding="UTF-8") as sites_json:
    sites_data = json.load(sites_json)

urls = gs.reader.read_range(URL_RANGE)
with open("result.txt","a",encoding="utf-8") as result_file:
            result_file.write("URL;Number1;Number2;VK;OK;WP;TG\n")

for site in sites_data["sites"]:
    row_ids = gs.reader.find_row_id_by_word(LOGIN_RANGE, site["login"])
    collector = SiteCollector()
    collector.set_options(driver)
    
    for row_id in row_ids:
        print(row_id)
        url = urls[row_id - 1][0]
        data = {}
        try:
            data = collector.get_data(url)
        except:
            pass

        with open("result.txt","a",encoding="utf-8") as result_file:
            if len(data) == 0:
                result_file.write(f"{url}; error;\n")
                continue
            result_file.write(f"{url};{';'.join(data['numbers'])};{data['vk']};{data['ok']};{data['wp']};{data['telegram']}\n")
        print("good")