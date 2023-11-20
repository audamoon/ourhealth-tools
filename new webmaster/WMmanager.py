from sheethelper.manager import SheetManager
import undetected_chromedriver as uc
from WMElement import WMElement
from WMController import WMController
from WMEnum import WMSheetCells
from datetime import datetime

class WMmanager:
    def __init__(self, driver: uc.Chrome, gs: SheetManager) -> None:
        self.LOG_TIME = f"{datetime.now().date()}-{datetime.now().hour}-{datetime.now().minute}"
        self.driver = driver
        self.gs = gs
        self.controller = WMController(driver, gs)

    def mod_launch(self, service: WMElement, mod):
        #Формируем дату для файла
        row_ids = self.gs.reader.find_row_id_by_word(WMSheetCells.STATUS, WMSheetCells.WORD_TO_START)
        service = service(self.controller)

        if len(row_ids) == 0:
            with open(f"logs/result{self.LOG_TIME}.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Нечего выполнять")

        for row_id in row_ids:
            service.start_mod(row_id, mod)
            result = service.get_result()
            with open(f"logs/result{self.LOG_TIME}.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Row;{row_id}:{result['status']}:{result['link']}\n")

    def collect_sites(self, amount_of_sites):
        links = self.controller.collect_sites(amount_of_sites)
        with open(f"logs/result{self.LOG_TIME}.txt", "a", encoding="UTF-8") as log_file:
                for link in links:
                    log_file.write(f"{link}\n")