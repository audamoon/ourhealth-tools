class GoogleSheetWriter:
    def set_options(self, service, sheet_id):
        self.service = service
        self.sheet_id = sheet_id

    def write_cell(self, range, value: str):
        """
        usage example: 

        write_cell("B1", value)

        ===================================

        if you want specify list name just add: "listname!" before range:

        write_cell("Sheet1!B1", value)
        """
        valueInputOption = 'USER_ENTERED'
        body = {
            'values': [[value]]
        }
        self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id,
                                                    range=range, valueInputOption=valueInputOption, body=body).execute()

    def write_range(self, column_range, value: list):
        """
        usage example: 

        write_range("B:B", list_with_values)

        ===================================

        if you want specify list name just add: "listname!" before range:

        write_range("Sheet1B:B", list_with_values)

        ===================================

        for fill all range with one word use:

        write_range(range, [your_word] * last_row_id)
        """
        if isinstance(value, list) == False:
            raise TypeError("value must be list")

        valueInputOption = 'RAW'
        body = {
            'values': [[value1] for value1 in value]
        }
        return self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id, range=column_range, valueInputOption=valueInputOption, body=body).execute()

