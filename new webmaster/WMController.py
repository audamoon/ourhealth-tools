from sheethelper.manager import SheetManager
import undetected_chromedriver as uc
from SheetConst import SheetConst
import time
import re

class WMController:
    BASIC_URI = "https://webmaster.yandex.ru/site/"
    PORT = "443"

    def __init__(self, driver: uc.Chrome, gs: SheetManager) -> None:
        self.driver = driver
        self.gs = gs
        self.domains = gs.reader.read_range(SheetConst.DOMAIN)
        self.additional = gs.reader.read_range(SheetConst.ADDITIONAL)

    def open_link(self, row_id, uri):
        domain_parts = re.findall(r'(https:)\/\/([a-z-.]+)[\/]?', self.domains[row_id-1][0], re.IGNORECASE)[0]
        print(f"{self.BASIC_URI}{domain_parts[0]}{domain_parts[1]}:{self.PORT}{uri}")
        time.sleep(10)