from gseleniumconf.chrome import ChromeConfigurator
from sheethelper.manager import SheetManager
from modules.SiteCollector import SiteCollector
import json

#добавить вк и ок
driver = ChromeConfigurator.get_driver()
gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs")

EMAIL_RANGE = "B:B"
URL_RANGE = "G:G"

with open ("collect/data/Sites.json", "r", encoding="UTF-8") as sites_json:
    sites = json.load(sites_json)

urls = gs.reader.read_range(URL_RANGE)
with open("result.txt","a",encoding="utf-8") as result_file:
            result_file.write("URL      N1      N2      WP      TG\n")
for site in sites["sites"]:
    row_ids = gs.reader.find_row_id_by_word(EMAIL_RANGE, site["email"])
    collector = SiteCollector()
    collector.set_options(driver, site["wp_xpath"], site["number_xpath"])
    
    for row_id in row_ids:
        url = urls[row_id - 1][0]
        data = {}
        try:
            data = collector.get_data(url)
        except:
            pass

        with open("result.txt","a",encoding="utf-8") as result_file:
            if len(data) == 0:
                result_file.write(f"{url}; error; error; error; error\n")
                continue
            if len(data["numbers"])  == 2:
                result_file.write(f"{url};{data['numbers'][0]};{data['numbers'][1]};{data['wp']};{data['telegram']}\n")
            if len(data["numbers"]) == 1:
                result_file.write(f"{url};{data['numbers'][0]};none;{data['wp']};{data['telegram']}\n")