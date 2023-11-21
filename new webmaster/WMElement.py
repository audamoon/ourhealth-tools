from abc import ABC, abstractmethod
from WMController import WMController
from WMEnum import WMWorkResults
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WMElement(ABC):
    URI: str
    status: str

    @abstractmethod
    def __init__(self, controller: WMController):
        self.controller = controller

    @abstractmethod
    def get_result(self) -> str:
        """
        Функция возвращает результат выполнения программы

        Пример использования:
        service.get_result()
        """
        return {'status': self.status, 'link': self.link}

    @abstractmethod
    def start_mod(self, row_id, mods) -> str:
        """
        Функция сначала ищет по row_id ссылку и открывает её, а затем старается выполнить функцию mod
        Возвращает строку, в которой находится результат выполнения
        service(row_id, mod)
        """
        self.additional = self.controller.get_additional(row_id)
        # открываем ссылку
        self.link = self.controller.get_link(row_id, self.URI)
        if (not self.link):
            self.status = WMWorkResults.INCORRECT_LINK
            return
        self.controller.open_link(self.link)
        # Выполняем нужную функцию
        for mod in mods:
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
    status: str = ""

    def __init__(self, controller: WMController):
        super().__init__(controller)
        self.functions = {"delete": self.delete, "add": self.add}

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
        INPUT_RSS_XPATH = "//input[@name='feedUrl']"
        INPUT_SUBMIT_XPATH = "//span[text()='Добавить']/parent::button"
        TURBO_ON_XPATH = "//div[text()='Откл']/parent::div"
        # Надо протестить в процессе работы
        MODAL_CONFIRM = "//span[text()='Да, включить']/parent::button"

        input_RSS = self.controller.driver.find_element(
            By.XPATH, INPUT_RSS_XPATH)
        input_RSS.click()
        input_RSS.clear()
        input_RSS.send_keys(self.additional)

        input_submit = self.controller.driver.find_element(
            By.XPATH, INPUT_SUBMIT_XPATH)
        input_submit.click()

        WebDriverWait(self.controller.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, TURBO_ON_XPATH)))
        turbo_on_btn = self.controller.driver.find_element(
            By.XPATH, TURBO_ON_XPATH)
        turbo_on_btn.click()

        try:
            WebDriverWait(self.controller.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, MODAL_CONFIRM)))
            yes_on_btn = self.controller.driver.find_element(
                By.XPATH, MODAL_CONFIRM)
            yes_on_btn.click()
        except:
            pass

        self.status = WMWorkResults.SUCCESS

