from sheethelper.modules.reader import GoogleSheetReader
from sheethelper.modules.logger import GoogleSheetLogger
from sheethelper.modules.writer import GoogleSheetWriter
import os


class SheetManager:
    CREDS_PATH = os.environ.get('PYTHONPATH').split(os.pathsep)[0] + "\\sheethelper\\creds\\service_account_creds.json"
    
    def __init__(self, sheet_id):
        """
        usage:

        gs = SheetManager("your_sheet_id")
        """
        self.__start_service(sheet_id)

    def __start_service(self, sheet_id):
        service = GoogleSheetLogger.get_service(self.CREDS_PATH)
        self.reader = GoogleSheetReader().get_self(service, sheet_id)
        self.writer = GoogleSheetWriter().get_self(service, sheet_id)

