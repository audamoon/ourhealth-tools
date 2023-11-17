from sheethelper.manager import SheetManager
import undetected_chromedriver as uc
from WMElement import WMElement
from SheetConst import SheetConst

class WMmanager:
    

    def __init__(self, driver: uc.Chrome, gs:SheetManager) -> None:
        self.driver = driver
        self.gs = gs
        

    def launch(self, service: WMElement = ""):
        row_ids = self.gs.reader.find_row_id_by_word("Sheet10!" + SheetConst.STATUS, SheetConst.WORD_TO_START)
        additional = self.gs.reader.read_range("Sheet10!" + SheetConst.ADDITIONAL)
        domens = self.gs.reader.read_range("Sheet10!" + SheetConst.DOMAIN)
        for row_id in row_ids:
            
        # service.get_result()


    def save_result():
        pass