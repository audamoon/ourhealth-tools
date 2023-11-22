import undetected_chromedriver as uc
from sheethelper.manager import SheetManager
from modules.WMElement import WMElement
from modules.WMController import WMController
from modules.WMEnum import WMSheetCells
from datetime import datetime


class WMManager:
    def __init__(self, driver: uc.Chrome, gs: SheetManager) -> None:
        self.LOG_TIME = f"{datetime.now().date()}-{datetime.now().hour}-{datetime.now().minute}"
        self.driver = driver
        self.gs = gs
        self.controller = WMController(driver, gs)

    def start(self, service: WMElement, mods):
        row_ids = self.gs.reader.find_row_id_by_word(
            WMSheetCells.STATUS, WMSheetCells.WORD_TO_START)
        service = service(self.controller)

        if len(row_ids) == 0:
            with open(f"logs/result{self.LOG_TIME}.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Нечего выполнять")

        for row_id in row_ids:
            service.start(row_id, mods)
            result = service.getResult()
            with open(f"logs/result{self.LOG_TIME}.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(
                    f"{row_id};{result['status']};{result['link']}\n")

    def getSites(self):
        links = self.controller.getSites()
        with open(f"logs/result{self.LOG_TIME}.txt", "a", encoding="UTF-8") as log_file:
            for link in links:
                log_file.write(f"{link}\n")

    def getMenu(self, data_origin, menu_type, project="domain_name"):
        self.controller.getMenu(data_origin, project, menu_type)

    def saveResult(self, file_path):
        self.controller.saveResult(file_path)