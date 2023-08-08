from func.google_sheet_mgr import SheetManager
from func.selenium_mgr import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class WebmasterManager:
    def __init__(self, driver, sheet_id) -> None:
        self.sm = driver
        self.gs = SheetManager(sheet_id)

    def bypass_counters(self, i):
        print("Row num: ", cell_num)
        url = self.gs.read_cell("A", True, i)
        url_splited = url.split("//")
        yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/indexing/crawl-metrika/"
        self.gs.write_cell("F", yandex_url, True, i)
        try:
            self.sm.driver.get(yandex_url)
            self.sm.driver.find_element(By.XPATH,'//span[text()="Установите на сайт счётчик Яндекс Метрики"]')
            self.gs.write_cell("E", "Не установлена яндекс метрика", True, i)
        except:
            try:
                elements = self.sm.driver.execute_script("let a = document.querySelectorAll('.tumbler__disabled-label');arr = new Array;for (let i = 0; i < a.length; i++) {if (window.getComputedStyle(a[i]).display != 'none'){arr.push(a[i])}};return arr;")
                if len(elements) != 0:
                    for el in elements:
                        el.click()
                        sleep(1)
                        self.gs.write_cell("E", "Добавлен", True, i)
                else:
                    self.gs.write_cell("E", "Уже был", True, i)
            except:
                self.gs.write_cell("E", "Чета не так", True, i)

    def add_region(self, i):
        url = self.gs.read_cell("A", True, i)
        url_splited = url.split("//")
        city_name = self.gs.read_cell("B", True, i)
        print(url,city_name)
        contact_url = url + "/contacts/"
        yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/serp-snippets/regions/"
        self.gs.write_cell("D", yandex_url, True, i)
        try:
            self.sm.driver.get(yandex_url)
            self.sm.el_by_xpath(
                '(//li[@class="regions-list__item"][text()="регион сайта не задан"])[2]')
            self.sm.el_by_xpath("(//button)[5]").click()
            self.sm.el_by_xpath("(//button)[6]").click()
            self.saveRegion(city_name, contact_url)
            self.gs.write_cell("C", "Добавлен", True, i)
        except:
            try:
                self.sm.el_by_xpath(
                    f"(//li[@class='regions-list__item'][contains(text(),'{city_name}')])")
                self.gs.write_cell("C", "Уже был", True, i)
                sleep(1)
            except:
                self.gs.write_cell("C", "Чета не так", True, i)
                sleep(1)

    def saveRegion(self, keys, contacts):
        try:
            self.sm.el_by_xpath("(//input[@class='input__control'])[1]").click()
            self.sm.el_by_xpath("(//input[@class='input__control'])[1]").send_keys(keys)
            sleep(1)
            self.sm.el_by_xpath("//span[@class='suggest2-item__text'][1]").click()
            self.sm.el_by_xpath("(//input[@class='input__control'])[2]").send_keys(contacts)
            sleep(1)
            self.sm.el_by_xpath(".//span[text()='Сохранить']/parent::button").click()
            sleep(3)
        except:
            self.sm.driver.refresh()
            sleep(4)


sm = SeleniumManager()
wm = WebmasterManager(sm,"1_lxCGttccBF3TMbEsuFHbsvQ-e9_x3Anl9zutX0xfQE")
for cell_num in range(1, 908):
    
