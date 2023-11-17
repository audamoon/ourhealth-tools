from google.oauth2 import service_account
from apiclient import discovery


class GoogleSheetLogger:
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']

    @classmethod
    def get_service(cls , path_to_creds):
        
        creds = service_account.Credentials.from_service_account_file(
            path_to_creds, scopes=cls.SCOPE)
        
        service = discovery.build('sheets', 'v4', credentials=creds)

        return service
