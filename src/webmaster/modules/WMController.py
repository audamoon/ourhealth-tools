import undetected_chromedriver as uc
import re
from selenium.webdriver.common.by import By
from sheethelper.manager import SheetManager
from modules.WMEnum import WMSheetCells
from modules.WMTableManager import WMMainMenu, WMTopMenu


class WMController:
    BASIC_URI = "https://webmaster.yandex.ru/site/"
    PORT = "443"
    PROTOCOL = "https"

    def __init__(self, driver: uc.Chrome, gs: SheetManager) -> None:
        self.driver = driver
        self.gs = gs
        self.domains = gs.reader.read_range(WMSheetCells.DOMAIN)
        self.additional = gs.reader.read_range(WMSheetCells.ADDITIONAL)

    def openLink(self, link):
        self.driver.get(link)

    def getDomain(self, row_id):
        return self.domains[row_id-1][0]

    def getLink(self, row_id, uri):
        domain_parts = re.findall(
            r'(https:)?\/?\/?([a-z-.]+)[\/]?', self.domains[row_id-1][0], re.IGNORECASE)
        return f"{self.BASIC_URI}{self.PROTOCOL}:{domain_parts[0][1]}:{self.PORT}{uri}" if len(domain_parts) != 0 else False

    def getAdd(self, row_id):
        if len(self.additional) > row_id:
            return self.additional[row_id-1][0]
        return ""

    def saveResult(self, file_path):
        with open(file_path, "r", encoding="UTF-8") as result_file:
            results = list(
                map(lambda x: x.split(";"), result_file.readlines()))

        g = 0
        results_ranged = [[]]

        for i in range(1, len(results)):

            if int(results[i - 1][0]) + 1 == int(results[i][0]):
                results_ranged[g].append(results[i-1])
                if (i == len(results) - 1):
                    results_ranged[g].append(results[i])

            if int(results[i - 1][0]) + 1 != int(results[i][0]):
                results_ranged[g].append(results[i-1])
                results_ranged.append([])
                g += 1
                if (i == len(results) - 1):
                    results_ranged[g].append(results[i])

        for result_range in results_ranged:
            min_index = int(result_range[0][0])
            max_index = int(result_range[len(result_range) - 1][0])
            self.gs.writer.write_range(WMSheetCells.get_range_between(
                "C", min_index, max_index), list(map(lambda x: x[1], result_range)))
            self.gs.writer.write_range(WMSheetCells.get_range_between(
                "D", min_index, max_index), list(map(lambda x: x[2].replace("\n", ""), result_range)))

    def getSites(self):
        ALL_SITES_LINK = "https://webmaster.yandex.ru/sites/?page="
        SITES_AMOUNT_XPATH = "//div[@class='SitesPage-Title']//span[@class='I18N']"
        SITE_LINK_XPATH = "//a[@class='Link SitesTableCell-Hostname']"

        self.driver.get(ALL_SITES_LINK)
        header_el = self.driver.find_element(By.XPATH, SITES_AMOUNT_XPATH)
        sites_amount = re.findall(r'[\d]+', header_el.text)

        pages = (int(sites_amount[0])/20)+1
        links = []

        for page_n in range(1, int(pages)+1):
            self.driver.get(f"{ALL_SITES_LINK}{page_n}")
            links_el = self.driver.find_elements(By.XPATH, SITE_LINK_XPATH)
            for el in links_el:
                links.append(el.text)
        return links

    def getMenu(self, data_origin, project, menu_type):
        self.openLink(data_origin)
        if menu_type == 'top':
            tm = WMTopMenu(self.driver, project)
            tm.getAllStructure()

        if menu_type == 'main':
            mm = WMMainMenu(self.driver, project)
            mm.getAllStructure()
