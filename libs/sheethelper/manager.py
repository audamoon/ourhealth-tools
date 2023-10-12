from sheethelper.modules.reader import GoogleSheetReader
from sheethelper.modules.logger import GoogleSheetLogger
from sheethelper.modules.writer import GoogleSheetWriter
import os


class SheetManager:

    CREDS_PATH = os.environ.get('PYTHONPATH').split(os.pathsep)[0] + "\\sheethelper\\creds\\service_account_creds.json"

    def __init__(self):
        self.reader = GoogleSheetReader()
        self.writer = GoogleSheetWriter()

    def start_service(self, sheet_id):
        """
        usage:

        gs = SheetManager()
        gs.start_service("your_sheet_id")
        """
        logger = GoogleSheetLogger()
        logger.start_service(self.CREDS_PATH, sheet_id)
        service = logger.get_service()
        
        self.reader.set_options(service, sheet_id)
        self.writer.set_options(service, sheet_id)