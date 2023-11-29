class WMSheetCells:
    WORD_TO_START = "ВЫПОЛНИТЬ"
    DOMAIN = "A:A"
    ADDITIONAL = "B:B"
    CITIES = "C:C"
    STATUS = "D:D"
    STATUS_SAVE = "D"
    LINK_TO_WM = "E:E"
    LINK_SAVE = 'E'

    def get_range_between(letter, first, second):
        return f"{letter}{first}:{letter}{second}"

class WMWorkResults:
    INCORRECT_LINK = "Указана некорректная ссылка/Нет ссылки"
    UNKNOW_FUNC = "Искомой функции в модуле не найдено"
    SUCCESS = "Выполнено успешно"
    WAS = "Выло выполнено"
