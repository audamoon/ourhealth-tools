from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import re
import json


class WMMenu(ABC):
    MENU_TYPE = ""

    def __init__(self, driver: uc.Chrome, project="domen_name") -> None:
        self.driver = driver
        self.project = project

    def getAllStructure(self):
        self._getStructure()
        self._getItemsName()

    def createMenu(self, site):
        self._createStructure()
        self._fillAllItems(site)

    def _getItemsName(self):
        inputs_xpath = f"//div[@class='turbo-setup-menu__{self.MENU_TYPE}']//input"
        result_file_path = f"tables/menu_structure_{self.MENU_TYPE}_{self.project}.txt"

        inputs = self.driver.find_elements(By.XPATH, inputs_xpath)

        open(result_file_path, 'w').close()

        for input in inputs:
            value = input.get_attribute("value")
            with open(result_file_path, "a", encoding="UTF-8") as table_file:
                table_file.write(value + '\n')

    def _fillAllItems(self, site):
        inputs_xpath = f"//div[@class='turbo-setup-menu__{self.MENU_TYPE}']//input"
        result_file_path = f"tables/menu_structure_{self.MENU_TYPE}_{self.project}.txt"

        with open(result_file_path, "r", encoding="UTF-8") as table_file:
            values = table_file.readlines()

        inputs = self.driver.find_elements(By.XPATH, inputs_xpath)

        for i in range(len(values)):
            input_value = values[i].replace('\n', '')
            if (re.match(r'https:\/\/.+[.][a-z]+', values[i])):
                site_uri = re.sub(r'https:\/\/.+[.][a-z]+', "", values[i])
                input_value = f"{site}{site_uri}"
            inputs[i].click()
            inputs[i].clear()
            inputs[i].send_keys(input_value)

    def _createStructure(self):
        pass

    def _getStructure(self):
        pass

    def addItem(self, level):
        pass


class WMTopMenu(WMMenu):
    MENU_TYPE = "top"

    def _getStructure(self):
        rows_xpath = f"//*[@class='turbo-setup-menu__{self.MENU_TYPE}']//tr[contains(@class,'sun-table__row')]"
        json_file_path = f"tables/menu_structure_{self.MENU_TYPE}_{self.project}.json"
        input_row = self.driver.find_elements(By.XPATH, rows_xpath)
        with open(json_file_path, "w") as table_json:
            table_json.write(str(len(input_row)))

    def _createStructure(self):
        json_file_path = f"tables/menu_structure_{self.MENU_TYPE}_{self.project}.json"
        with open(json_file_path, "r") as table_json:
            amount = json.loads(table_json.read())
        for i in range(amount):
            self.addItem()

    def addItem(self, level=''):
        add_menu_btn_xpath = f"(//*[@class='turbo-setup-menu__{self.MENU_TYPE}']//button)[last()]"
        self.driver.find_element(By.XPATH, add_menu_btn_xpath).click()


class WMMainMenu(WMMenu):
    MENU_TYPE = "main"

    def _createStructure(self):
        json_file_path = f"tables/menu_structure_{self.MENU_TYPE}_{self.project}.json"
        with open(json_file_path, "r") as table_json:
            levels = json.loads(table_json.read())
        for level in levels:
            self.addItem(level)

    def _getStructure(self):
        rows_xpath = f"//*[@class='turbo-setup-menu__{self.MENU_TYPE}']//tr[contains(@class,'sun-table__row')]"
        json_file_path = f"tables/menu_structure_{self.MENU_TYPE}_{self.project}.json"

        input_row = self.driver.find_elements(By.XPATH, rows_xpath)

        with open(json_file_path, "w") as table_json:
            json_str = json.dumps(list(map(lambda x: int(re.findall(
                r'level_([\d])', x.get_attribute("class"))[0]), input_row)))
            table_json.write(json_str)

    def addItem(self, level):
        menu_xpath = f"(//*[@class='turbo-setup-menu__{self.MENU_TYPE}']"
        menu_element_xpath = f"//tr[contains(@class,'sun-table__row_menu-level_{level-1}')][last()]"
        add_sub_btn_xpath = f"//span[contains(@class,'link_menu-level_{level-1}')])[last()]"
        add_menu_btn_xpath = f"//button[contains(@class,'button_menu-level_{level}')])[last()]"

        try:
            self.driver.find_element(
                By.XPATH, menu_xpath + menu_element_xpath + add_sub_btn_xpath).click()
            return
        except:
            pass

        try:
            self.driver.find_element(
                By.XPATH, menu_xpath + add_menu_btn_xpath).click()
            return
        except:
            pass
