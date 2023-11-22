from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import re
import json


class WMTable(ABC):
    TABLE_TYPE = ""

    def __init__(self, driver: uc.Chrome, project) -> None:
        self.driver = driver
        self.project = project

    def read_menu_levels(self):
        pass

    def collect_menu_inputs(self):
        inputs_xpath = f"//div[@class='turbo-setup-menu__{type}']//input"
        result_file_path = f"tables/menu_structure_{type}_{self.project}.txt"

        inputs = self.driver.find_elements(By.XPATH, inputs_xpath)
        with open(result_file_path, "w", encoding="UTF-8") as table_file:
            pass

        for input in inputs:
            value = input.get_attribute("value")
            with open(result_file_path, "a", encoding="UTF-8") as table_file:
                table_file.write(value + '\n')

    def input_values_in_menus(self, site):
        inputs_xpath = f"//div[@class='turbo-setup-menu__{type}']//input"
        result_file_path = f"tables/menu_structure_{type}_{self.project}.txt"

        with open(result_file_path, "r", encoding="UTF-8") as table_file:
            values = table_file.readlines()

        inputs = self.driver.find_elements(By.XPATH, inputs_xpath)

        for i in range(len(values)):
            input_value = values[i]
            if (re.match(r'https:\/\/.+[.][a-z]+', values[i])):
                site_uri = re.sub(r'https:\/\/.+[.][a-z]+', "", values[i])
                input_value = f"{site}{site_uri}"
            inputs[i].click()
            inputs[i].clear()
            inputs[i].send_keys(input_value)

    def create_table(self):
        json_file_path = f"tables/menu_structure_{type}_{self.project}.json"
        with open(json_file_path, "r") as table_json:
            levels = json.loads(table_json.read())

        self.add_item(type)

    def add_item(self, *level):
        pass


class WMTopTable(WMTable):
    TABLE_TYPE = "top"

    def read_menu_levels(self):
        rows_xpath = f"//*[@class='turbo-setup-menu__{self.TABLE_TYPE}']//tr[contains(@class,'sun-table__row')]"
        json_file_path = f"tables/menu_structure_{self.TABLE_TYPE}_{self.project}.json"

        input_row = self.driver.find_elements(By.XPATH, rows_xpath)
        with open(json_file_path, "w") as table_json:
            table_json.write(input_row)

    def add_item(self, type):
        add_menu_btn_xpath = f"(//*[@class='turbo-setup-menu__{type}']//button)[last()]"
        self.driver.find_element(By.XPATH, add_menu_btn_xpath).click()


class WMMainTable(WMTable):
    TABLE_TYPE = "main"

    def read_menu_levels(self):
        rows_xpath = f"//*[@class='turbo-setup-menu__{self.TABLE_TYPE}']//tr[contains(@class,'sun-table__row')]"
        json_file_path = f"tables/menu_structure_{self.TABLE_TYPE}_{self.project}.json"

        input_row = self.driver.find_elements(By.XPATH, rows_xpath)

        with open(json_file_path, "w") as table_json:
            json_str = json.dumps(list(map(lambda x: int(re.findall(
                r'level_([\d])', x.get_attribute("class"))[0]), input_row)))
            table_json.write(json_str)

    def add_item(self, type, level):
        menu_xpath = f"(//*[@class='turbo-setup-menu__{type}']"
        menu_element_xpath = f"//tr[contains(@class,'sun-table__row_menu-level_{level-1}')][last()]"
        add_menu_btn_xpath = f"//button[contains(@class,'button_menu-level_{level}')])[last()]"
        add_sub_btn_xpath = f"//span[contains(@class,'link_menu-level_{level-1}')])[last()]"
        add_menu_el = self.driver.find_element(By.XPATH, menu_xpath + add_menu_btn_xpath)
        add_sub_el = self.driver.find_element(By.XPATH, menu_xpath + menu_element_xpath + add_sub_btn_xpath)

        if add_sub_el:
            add_sub_el.click()
            return
        if add_menu_el:
            add_menu_el.click()