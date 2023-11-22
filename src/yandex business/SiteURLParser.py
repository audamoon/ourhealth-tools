import bs4
import time
from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator


gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs")
driver = ChromeConfigurator.get_driver()

url_rows = gs.reader.find_row_id_by_word("G:G","НЕТ")

for url_row in url_rows:
    url = gs.reader.read_сell(f"D{url_row}")
    driver.get(url)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html,"html.parser")
    site_url = soup.find(class_="business-urls-view__text")
    gs.writer.write_cell(f"G{url_row}", site_url.text)
    time.sleep(1) 
