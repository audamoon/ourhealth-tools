from selenium.webdriver.common.by import By
from time import sleep
import re
import os
import json


class NetCatManager:
    iframes = {'left': 'treeIframe', 'center': 'mainViewIframe'}

    def __init__(self, url, driver) -> None:
        self.url = url
        self.driver = driver
        self.get_main_id()

    def switch_frame(self, view_name):
        if view_name == 'default':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.iframes[view_name])

    def open_netcat(self):
        self.driver.get(self.url)

    def open_subdivisions(self, subs):
        for sub in subs:
            sub.click()

    def get_main_id(self):
        main_link = self.url
        self.main_id = "".join(re.findall(r'([^()]+)', main_link)[1])


class subdivision:

    def __init__(self, subdivision_url, subdivision_name) -> None:
        self.url = subdivision_url
        self.name = subdivision_name


class subdivisionFactory:

    def makesubdivision(driver, subdivision_name):

        return subdivision(subdivision_url=driver.current_url, subdivision_name=subdivision_name)


class NetCatFunctions:
    old_words = ["Татьяны Карповой", "Карповой",
                 "Москвы", "г. Москва", "в Москве"]
    new_words = ["Екатерины Стукаловой", "Стукаловой",
                 "Санкт-Петербурга", "г. Санкт-Петербург", "в Санкт-Петербурге"]

    def __init__(self, netcat_mgr, selenium_mgr) -> None:
        self.nm = netcat_mgr
        self.sm = selenium_mgr

    def choose_file_path(self, path):
        self.folder_path = path

    def open_subs(self, xpath=""):
        """Открывает видимые разделы

        Дополнительно можно указать XPATH, где крайний элемент должен быть li
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")
        if xpath == "":
            xpath = f"//img[@alt='Раскрыть список']"
        else:
            xpath = xpath + f"/img[@alt='Раскрыть список']"
        self.nm.open_subdivisions(self.sm.els_by_xpath(xpath))

    def write_active_subs(self):
        """Позволяет записать активные разделы в файл
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")

        with open(self.folder_path + "/temp/subdivisions.json", "w", encoding="UTF-8") as subdivisions_file:
            subs = self.sm.els_by_xpath("//a[@class='menu_left_a active']")
            subs_dict = []
            for sub in subs:
                obj = {
                    "sub_name": sub.get_attribute('title'),
                }
                subs_dict.append(obj)
            json.dump(subs_dict, subdivisions_file, ensure_ascii=False)

    def choose_subs(self):
        """Перезаписывает файл, оставляя в нём только выбранные разделы
        """
        choosed_subs = input("Введите выбранные разделы через запятую: ")
        choosed_subs = choosed_subs.split(",")
        with open(self.folder_path + "/temp/subdivisions.json", "r", encoding="UTF-8") as subdivisions_file:
            subs = json.load(subdivisions_file)
        choosed_subs_to_json = []
        with open(self.folder_path + "/temp/subdivisions.json", "w", encoding="UTF-8") as subdivisions_file:
            for choosed_sub in choosed_subs:
                for sub in subs:
                    if choosed_sub in sub["sub_name"]:
                        choosed_subs_to_json.append(sub)
            json.dump(choosed_subs_to_json,
                      subdivisions_file, ensure_ascii=False)

    def get_URl(self):
        """Записывает в файл URL выбранных разделов.

        Важное условие: выбранные разделы должны быть видимыми
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")

        with open(self.folder_path + "/temp/subdivisions.json", "r", encoding="UTF-8") as subdivisions_file:
            choosed_subs = json.load(subdivisions_file)

        for choosed_sub in choosed_subs:
            choosed_sub_el = self.sm.el_by_xpath(
                f"//a[contains(@title,'{choosed_sub['sub_name']}')]")
            choosed_sub_el.click()
            choosed_sub.update({"sub_URL": self.sm.driver.current_url})
        with open(self.folder_path + "/temp/subdivisions.json", "w", encoding="UTF-8") as subdivisions_file:
            json.dump(choosed_subs, subdivisions_file, ensure_ascii=False)

    def get_fields(self):
        self.nm.switch_frame("default")
        string_area = self.sm.els_by_xpath(
            "//div[@class='nc-field nc-field-type-string']")
        textarea = self.sm.els_by_xpath(
            "//div[@class='nc-field nc-field-type-text']")
        string_to_json = []
        textarea_to_json = []
        for str in string_area:
            el = str.find_element(
                By.XPATH, "./span[@class='nc-field-caption']")
            string_to_json.append(
                {
                    "string_name": el.text,
                    "string_id": el.get_attribute("id")
                }
            )
        for text_el in textarea:
            el = text_el.find_element(
                By.XPATH, "./span[@class='nc-field-caption']")
            textarea_to_json.append(
                {
                    "textarea_name": el.text,
                    "textarea_id": el.get_attribute("id")
                }
            )
        with open(self.folder_path + "/temp/forms.json", "w", encoding="UTF-8") as forms_file:
            compiled = {
                "string_array": string_to_json,
                "text_array": textarea_to_json
            }
            json.dump(compiled, forms_file, ensure_ascii=False)

    def change_word_in_fields(self):
        self.nm.switch_frame("default")
        with open(self.folder_path + "/temp/forms.json", "r", encoding="UTF-8") as forms_file:
            forms_name = json.load(forms_file)
        for str_names in forms_name["string_array"]:
            el = self.sm.el_by_xpath(
                f"//span[@id='{str_names['string_id']}']/parent::div")
            input = el.find_element(By.XPATH, "./input")

            input_text = input.get_attribute("value")
            if input_text == False:
                continue
            input_text = self.change_doctor(
                input_text, self.old_words, self.new_words)

            input.click()
            input.clear()
            input.send_keys(input_text)

        for text_names in forms_name["text_array"]:
            el = self.sm.el_by_xpath(
                f"//span[@id='{text_names['textarea_id']}']/parent::div")

            textarea_text = el.find_element(
                By.XPATH, "./textarea").get_attribute("textContent")
            if textarea_text == False:
                continue

            textarea_text = self.change_doctor(
                textarea_text, self.old_words, self.new_words)

            source_btn = el.find_element(
                By.XPATH, ".//a[@class='cke_button cke_button__source cke_button_off']")

            source_btn.click()
            textarea = el.find_element(By.XPATH, ".//textarea[@dir]")
            textarea.click()
            textarea.clear()
            textarea.send_keys(textarea_text)
            source_btn.click()

        savebtn = self.sm.el_by_xpath(
            f"//div[@class='nc-modal-dialog-footer']/button[text()='Сохранить']")
        savebtn.click()

    def get_sub_children(self):
        """Находит детей выбранных разделов и записывает их в файл
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")
        with open(os.getcwd() + "/temp/subdivisions.json", "r", encoding="UTF-8") as subdivisions_file:
            choosed_subs = json.load(subdivisions_file)
        subs_to_json = []
        for choosed_sub in choosed_subs:
            choosed_sub_el = self.sm.el_by_xpath(
                f"//a[contains(@title,'{choosed_sub['sub_name']}')]")
            choosed_sub_el.click()
            subs_to_json.append(choosed_sub)
            sleep(1)

            child_els_name = choosed_sub_el.find_element(
                By.XPATH, './parent::li').find_elements(By.XPATH, "./ul/li/a[@class='menu_left_a active']")

            for el in child_els_name:
                subs_to_json.append({"sub_name": el.get_attribute('title')})

        with open(os.getcwd() + "/temp/subdivisions.json", "w", encoding="UTF-8") as subdivisions_file:
            json.dump(subs_to_json, subdivisions_file, ensure_ascii=None)

    def change_menu_tab(self, main_tab, is_additional_tabs=False, additional_tab=""):
        self.nm.switch_frame("default")
        choosed_tab = self.sm.el_by_xpath(
            f"//ul[@id='mainViewTabs']/li/span[text()='{main_tab}']")
        choosed_tab.click()
        sleep(1)
        if is_additional_tabs:
            choosed_additional_tab = self.sm.el_by_xpath(
                f"//ul[@id='mainViewToolbar']/div/li[text()='{additional_tab}']")
            choosed_additional_tab.click()

    def seo_change(self):
        self.change_menu_tab("Настройки", True, "SEO/SMO")
        sleep(1)
        self.nm.switch_frame("center")
        self.change_input("//input[@name='title']")
        self.change_input("//input[@name='h1']")
        edit_btn = self.sm.el_by_xpath(
            "//div[contains(text(),'Описание страницы для поисковиков:')]/div/div[@class='cm_switcher']/span[1]/input")
        edit_btn.click()
        textarea = self.sm.el_by_xpath("//textarea[@id='description']")
        textarea_text = self.change_doctor(
            textarea.text, self.old_words, self.new_words)
        textarea.click()
        textarea.clear()
        textarea.send_keys(textarea_text)
        self.nm.switch_frame("default")
        savebtn = self.sm.el_by_xpath("//div[@title='Сохранить изменения']")
        savebtn.click()

    def edit_sub(self):
        self.nm.switch_frame("center")
        edit_btn = self.sm.el_by_xpath(
            "//i[@class='nc-icon nc--edit']/parent::a")
        edit_btn.click()

    def change_input(self, input_path):
        input = self.sm.el_by_xpath(input_path)
        input_text = input.get_attribute("value")
        input_text = self.change_doctor(
            input_text, self.old_words, self.new_words)
        input.click()
        input.clear()
        input.send_keys(input_text)

    def change_doctor(self, text, old_words, new_words):
        for i in range(len(old_words)):
            if old_words[i] in text:
                text = text.replace(old_words[i], new_words[i])
        return text

    def change_all_names(self):
        with open(os.getcwd() + "/temp/subdivisions.json", "r", encoding="UTF-8") as subdivisions_file:
            choosed_subs = json.load(subdivisions_file)
        for sub in choosed_subs:
            self.sm.driver.get(sub["sub_URL"])
            sleep(3)
            self.edit_sub()
            sleep(1)
            self.change_word_in_fields()
            sleep(3)
            self.seo_change()
            sleep(3)
