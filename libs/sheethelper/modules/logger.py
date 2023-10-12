from google.oauth2 import service_account
from apiclient import discovery


class GoogleSheetLogger:
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']

    def get_service(self):
        return self.service

    def start_service(self, path_to_creds, sheet_id):
        self.__set_creds(path_to_creds)
        self.__set_sheet_id(sheet_id)
        self.__service_init()

    def __set_sheet_id(self, sheet_id):
        self.sheet_id = sheet_id

    def __set_creds(self, path_to_creds: str):
        self.creds = service_account.Credentials.from_service_account_file(
            path_to_creds, scopes=self.SCOPE)

    def __service_init(self):
        self.service = discovery.build('sheets', 'v4', credentials=self.creds)