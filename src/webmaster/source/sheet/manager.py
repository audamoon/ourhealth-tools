from source.sheet.modules.logger import GoogleSheetLogger
from source.sheet.modules.writer import GoogleSheetWriter
from source.sheet.modules.reader import GoogleSheetReader


class GoogleSheetManager:
    def __init__(self):
        self.logger = GoogleSheetLogger()
        self.reader = GoogleSheetReader()
        self.writer = GoogleSheetWriter()

    def start_service(self, path_to_creds, sheet_id):
        """
        usage:

        GoogleSheetManager().start_service("creds/creds.json", "GHEIGEIN#I$#f253234safEhfe")
        """
        self.logger.start_service(path_to_creds, sheet_id)
        service = self.logger.get_service()
        self.reader.set_options(service, sheet_id)
        self.writer.set_options(service, sheet_id)