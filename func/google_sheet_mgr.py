#Google Sheet
from google.oauth2 import service_account
from apiclient import discovery

class SheetManager:

    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

    def __init__(self,sheet_id):
        self.sheet_id = sheet_id
        self.set_creds()
        self.start_service()

    def set_creds(self):
        self.creds = service_account.Credentials.from_service_account_file('creds/service_account_creds.json', scopes=self.scope)

    def start_service(self):
        self.service = discovery.build('sheets', 'v4', credentials=self.creds)

    def read_cell(self,range,isloop=False,i=None):
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=(f"{range}{i}" if isloop else range)).execute()['values'][0][0]
    
    def write_column_from_array(self,range,value):
        valueInputOption = 'RAW'
        body = {
            'values':[[value1] for value1 in value]#[[value]]
        }
        return self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id,range=range,valueInputOption=valueInputOption,body=body).execute()
    
    def write_cell(self,range,value,isloop=False,i=None):
        valueInputOption = 'USER_ENTERED'
        body = {
            'values':[[value]]
        }
        return self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id,range=(f"{range}{i}" if isloop else range),valueInputOption=valueInputOption,body=body).execute()
    
    def get_values(self,range):
        real_range = f"{range}:{range}"
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=real_range).execute()['values']

    def find_cell_with_word(self,sheet_range,word):
        status_from_sheet = self.get_values(sheet_range)
        array_of_n = []
        for i in range(len(status_from_sheet)):
            if status_from_sheet[i][0] == word:
                el_n = i + 1
                array_of_n.append(el_n)
        return array_of_n