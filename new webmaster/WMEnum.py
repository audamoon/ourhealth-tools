class WMSheetCells:
    WORD_TO_START = "ВЫПОЛНИТЬ"
    DOMAIN = "A:A"
    ADDITIONAL = "B:B"
    STATUS = "C:C"
    LINK_TO_WM = "D:D"

    def get_range_between(letter, first, second):
        return f"{letter}{first}:{letter}{second}"

class WMWorkResults:
    INCORRECT_LINK = "Указана некорректная ссылка/Нет ссылки"
    UNKNOW_FUNC = "Искомой функции в модуле не найдено"
    SUCCESS = "Выполнено успешно"