class GoogleSheetReader:

    def set_options(self, service, sheet_id):
        self.service = service
        self.sheet_id = sheet_id

    def read_сell(self, range):
        """
        usage example: 

        read_cell("B1", value)

        ===================================

        if you want specify list name just add: "listname!" before range:

        read_cell("Sheet1!B1", value)
        """
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=range).execute()['values'][0][0]

    def read_range(self, range):
        """
        usage example: 

        read_range("B:B")

        ===================================

        if you want specify list name just add: "listname!" before range:

        read_range("Sheet1!B1:B5")
        """
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=range).execute()['values']

    def find_row_id_by_word(self, sheet_range, word):
        """
        usage example:

        find_row_id_by_word("E:E", "TRUE")

        ===================================

        if you want specify list name just add: "listname!" before range:

        find_row_id_by_word("Sheet1!E:E", "TRUE")
        """
        status_from_sheet = self.read_range(sheet_range)
        row_numbers = []
        for i in range(len(status_from_sheet)):
            try:
                if status_from_sheet[i][0] == word:
                    el_n = i + 1
                    row_numbers.append(el_n)
            except:
                pass
        return row_numbers
    
    def find_row_id_by_two_word(self, first_sheet_range,second_sheet_range, first_word, second_word):
        """
        usage example:

        find_row_id_by_two_word("E:E", "G:G", "TRUE", "1")

        ===================================

        if you want specify list name just add: "listname!" before range:

        find_row_id_by_word("Sheet1!E:E","Sheet1!G:G", "TRUE", "1")
        """
        status_from_sheet_first = self.read_range(first_sheet_range)
        status_from_sheet_second = self.read_range(second_sheet_range)
        
        row_numbers = []
        for i in range(len(status_from_sheet_first)):
            try:
                if (status_from_sheet_first[i][0] == first_word) and (status_from_sheet_second[i][0] == second_word):
                    el_n = i + 1
                    row_numbers.append(el_n)
            except:
                pass
        return row_numbers