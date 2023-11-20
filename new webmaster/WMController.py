from sheethelper.manager import SheetManager
import undetected_chromedriver as uc
from WMEnum import WMSheetCells
from selenium.webdriver.common.by import By
import time
import re

class WMController:
    BASIC_URI = "https://webmaster.yandex.ru/site/"
    PORT = "443"

    def __init__(self, driver: uc.Chrome, gs: SheetManager) -> None:
        self.driver = driver
        self.gs = gs
        self.domains = gs.reader.read_range(WMSheetCells.DOMAIN)
        self.additional = gs.reader.read_range(WMSheetCells.ADDITIONAL)

    def open_link(self, link):
        self.driver.get(link)

    def get_link(self, row_id, uri):
        domain_parts = re.findall(r'(https:)\/\/([a-z-.]+)[\/]?', self.domains[row_id-1][0], re.IGNORECASE)
        return f"{self.BASIC_URI}{domain_parts[0][0]}{domain_parts[0][1]}:{self.PORT}{uri}" if len(domain_parts) != 0  else False

    def get_additional(self, row_id):
        return self.additional[row_id-1][0]

    def collect_sites(self, amount_of_sites):
        pages = (amount_of_sites/20)+1
        links = []
        for page_n in range(1, int(pages)+1):
            self.driver.get(
                f"https://webmaster.yandex.ru/sites/?page={page_n}")
            links_el = self.driver.find_elements(
                By.XPATH, f"//a[@class='Link SitesTableCell-Hostname']")
            for el in links_el:
                links.append(el.text)
        return links