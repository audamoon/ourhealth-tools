from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.WMController import WMController
from modules.WMEnum import WMWorkResults
from modules.WMTableManager import WMMainMenu, WMTopMenu


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
        self.city = self.controller.getCity(row_id)
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
        SUCC_MESSAGE = "//*[text()='Общая информация о сайте сохранена']"
        SAVE_BTN = "//button[contains(@class,'form__submit')]"

        mm = WMMainMenu(self.controller.driver, self.additional)
        mm.createMenu(self.domain)

        self.controller.driver.find_element(By.XPATH, SAVE_BTN).click()

        WebDriverWait(self.controller.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, SUCC_MESSAGE)))

        self.status = WMWorkResults.SUCCESS


class Counter(WMElement):
    URI = '/indexing/crawl-metrika/'
    status: str = ""

    def __init__(self, controller: WMController):
        super().__init__(controller)
        self.functions = {"bypass": self.bypass}

    def bypass(self):
        elements = self.controller.driver.execute_script(
            "let a = document.querySelectorAll('.tumbler__disabled-label');arr = new Array;for (let i = 0; i < a.length; i++) {if (window.getComputedStyle(a[i]).display != 'none'){arr.push(a[i])}};return arr;")
        if len(elements) != 0:
            for el in elements:
                el.click()
        self.status = WMWorkResults.SUCCESS


class Region(WMElement):
    URI = "/serp-snippets/regions/"
    status: str = ""

    def __init__(self, controller: WMController):
        super().__init__(controller)
        self.functions = {"add": self.add}

    def add(self):
        CHECK_REG_XPATH = '(//li[@class="RegionsList-Item"]/*[text()="регион сайта не задан"])[2]'
        PLUS_XPATH = "//button[contains(@class,'RegionsPage-PlusButton')]"
        ADD_REG_BTN_XPATH = "//span[text()='Добавить регион']/parent::span/parent::button"
        INPUT_REG_XPATH = "(//input[@class='yc-text-input__control yc-text-input__control_type_input'])[3]"
        FIRST_SUGGEST_XPATH = "//div[@class='RegionSuggest-Item'][1]"
        CONTACT_INPUT_XPATH = "//input[@class='yc-text-input__control yc-text-input__control_type_input'][@type='url']"
        SAVE_XPATH = "//span[text()='Сохранить']/parent::span/parent::button"
        CHECK_SAVE_XPATH = "//*[text()='Заявка принята в обработку']"
        controller = self.controller

        try:
            controller.driver.find_element(By.XPATH, CHECK_REG_XPATH)
        except:
            self.status = WMWorkResults.WAS
            return

        controller.driver.find_element(By.XPATH, PLUS_XPATH).click()
        WebDriverWait(controller.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ADD_REG_BTN_XPATH)))
        controller.driver.find_element(By.XPATH, ADD_REG_BTN_XPATH).click()
        WebDriverWait(controller.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, INPUT_REG_XPATH)))
        input_reg = controller.driver.find_element(By.XPATH, INPUT_REG_XPATH)
        input_reg.click()
        input_reg.clear()
        input_reg.send_keys(self.city)
        WebDriverWait(controller.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, FIRST_SUGGEST_XPATH)))
        controller.driver.find_element(By.XPATH, FIRST_SUGGEST_XPATH).click()
        input_contact = controller.driver.find_element(
            By.XPATH, CONTACT_INPUT_XPATH)
        input_contact.click()
        input_contact.clear()
        input_contact.send_keys(self.additional)
        controller.driver.find_element(By.XPATH,  SAVE_XPATH).click()
        WebDriverWait(controller.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, CHECK_SAVE_XPATH)))
        controller.driver.find_element(By.XPATH,  CHECK_SAVE_XPATH)
        self.status = WMWorkResults.SUCCESS


class Sitemap(WMElement):
    RI = "/indexing/sitemap/"
    status: str = ""

    def reload(self):
        CHECK_INFO_XPATH = "//div[@class='tooltip__content'][text()='Отправить файл Sitemap на переобход']"
        RELOAD_BTN_XPATH = "//button[contains(@class,'button_size_xs')]/parent::div"
        CHECK_SEND_XPATH = "//div[@class='tooltip__content'][contains(text(),'Файл был отправлен на переобход')]"
        controller = self.controller
        WebDriverWait(controller.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, CHECK_INFO_XPATH)))
        controller.driver.find_element(By.XPATH, RELOAD_BTN_XPATH).click()
        WebDriverWait(controller.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, CHECK_SEND_XPATH)))
        self.status = WMWorkResults.SUCCESS

    def delete(self):
        DELETE_BTN_XPATH = "//button[@aria-label='Удалить']"
        controller = self.controller
        WebDriverWait(controller.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, DELETE_BTN_XPATH)))
        controller.driver.find_element(By.XPATH, DELETE_BTN_XPATH).click()
        self.status = WMWorkResults.SUCCESS

    def add(self):
        SITEMAP_INPUT_XPATH = "//input[@name='sitemapUrl']"
        ADD_BTN_XPATH = "//span[@class='button__text'][text()='Добавить']/parent::button"
        CHECK_SUCCESS = "//p[@class='sitemap-files__queue-title'][text()='Очередь на обработку']"
        controller = self.controller
        WebDriverWait(controller.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, SITEMAP_INPUT_XPATH)))
        input_btn = controller.driver.find_element(
            By.XPATH, SITEMAP_INPUT_XPATH)
        input_btn.click()
        input_btn.clear()
        input_btn.send_keys(self.additional)
        controller.driver.find_element(By.XPATH, ADD_BTN_XPATH)
        WebDriverWait(controller.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, CHECK_SUCCESS)))
        self.status = WMWorkResults.SUCCESS
