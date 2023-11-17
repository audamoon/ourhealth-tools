from sheethelper.manager import SheetManager
import undetected_chromedriver as uc
from WMElement import WMElement
from WMController import WMController
from SheetConst import SheetConst


class WMmanager:
    def __init__(self, driver: uc.Chrome, gs: SheetManager) -> None:
        self.driver = driver
        self.gs = gs
        self.controller = WMController(driver, gs)

    def launch(self, service: WMElement = ""):
        row_ids = self.gs.reader.find_row_id_by_word(SheetConst.STATUS, SheetConst.WORD_TO_START)
        service =  service(self.controller)
       
        for row_id in row_ids:
            service.start(row_id)
            service.get_result()

    def save_result():
        pass
