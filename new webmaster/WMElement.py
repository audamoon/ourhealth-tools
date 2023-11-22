from abc import ABC, abstractmethod
from WMController import WMController
from WMEnum import WMWorkResults
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from WMTableManager import WMMainMenu, WMTopMenu


class WMElement(ABC):
    URI: str
    status: str

    def __init__(self, controller: WMController):
        self.controller = controller

    def getResult(self) -> str:
        """
        Функция возвращает результат выполнения программы

        Пример использования:
        service.get_result()
        """
        return {'status': self.status, 'link': self.link}

    def start(self, row_id, mods) -> str:
        """
        Функция сначала ищет по row_id ссылку и открывает её, а затем старается выполнить функцию mod
        Возвращает строку, в которой находится результат выполнения
        service(row_id, mod)
        """
        self.domain = self.controller.getDomain(row_id)
        self.additional = self.controller.getAdd(row_id)
        self._openLink(row_id)
        # Выполняем нужную функцию
        for mod in mods:
            try:
                self.functions[mod]()
            except Exception as e:
                self.status = e

    def _openLink(self, row_id):
        self.link = self.controller.getLink(row_id, self.URI)
        if (not self.link):
            self.status = WMWorkResults.INCORRECT_LINK
            return

        self.controller.openLink(self.link)

    def _setURI(self, new_URI):
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

    def getResult(self) -> str:
        return super().getResult()

    def start(self, row_id, mods) -> str:
        return super().start(row_id, mods)

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

class TurboMenu(WMElement):
    URI = '/turbo/settings/menu/'
    status: str = ""

    def __init__(self, controller: WMController):
        super().__init__(controller)
        self.functions = {"top": self.addTop, "main": self.addMain}

    def getResult(self) -> str:
        return super().getResult()

    def start(self, row_id, mods) -> str:
        return super().start(row_id, mods)

    def addTop(self):
        tm = WMTopMenu(self.controller.driver, self.additional)
        tm.createMenu(self.domain)
        self.status = WMWorkResults.SUCCESS

    def addMain(self):
        mm = WMMainMenu(self.controller.driver, self.additional)
        mm.createMenu(self.domain)
        self.status = WMWorkResults.SUCCESS

class Counter(WMElement):
    def bypass():
        pass

class Region(WMElement):
    def add():
        pass

class Sitemap(WMElement):
    def reload():
        pass
    
    def delete():
        pass

    def add():
        pass