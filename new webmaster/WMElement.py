from abc import ABC, abstractmethod
from WMController import WMController
from WMEnum import WMWorkResults
from selenium.webdriver.common.by import By


class WMElement(ABC):
    URI: str
    status : str

    @abstractmethod
    def __init__(self, controller: WMController):
        self.controller = controller

    @abstractmethod
    def get_result(self)-> str:
        """
        Функция возвращает результат выполнения программы

        Пример использования:
        service.get_result()
        """
        return {'status':self.status, 'link':self.link}

    @abstractmethod
    def start_mod(self, row_id, mod) -> str:
        """
        Функция сначала ищет по row_id ссылку и открывает её, а затем старается выполнить функцию mod
        Возвращает строку, в которой находится результат выполнения
        service(row_id, mod)
        """
        self.additional = self.controller.get_additional(row_id)
        #открываем ссылку
        self.link = self.controller.get_link(row_id, self.URI)
        if (not self.link):
            self.status = WMWorkResults.INCORRECT_LINK
            return
        self.controller.open_link(self.link)
        #Выполняем нужную функцию
        try:
            self.functions[mod]()
        except Exception as e:
            self.status = e 

    @abstractmethod
    def _change_URI(self, new_URI):
        """
        Функция заменяет URI по-умолчанию
        """
        self.URI = new_URI


class Turbo(WMElement):
    URI = "/turbo/sources/"
    status : str = ""

    def __init__(self, controller: WMController):
        super().__init__(controller)
        self.functions = {"delete":self.delete,"add":self.add}

    def get_result(self) -> str:
        return super().get_result()

    def start_mod(self, row_id, mod) -> str:
        return super().start_mod(row_id, mod)

    def _change_URI(self, new_URI):
        return super()._change_URI(new_URI)

    def delete(self):
        deleteBtns = self.controller.driver.find_elements(
            By.XPATH, "//button[contains(@aria-label, 'Удалить')]")
        for deletebtn in deleteBtns:
            deletebtn.click()
            self.controller.driver.find_element(
                By.XPATH, "//span[text()='Удалить']/parent::button").click()
        self.status = WMWorkResults.SUCCESS
    
    def add(self):
        print(self.additional)
