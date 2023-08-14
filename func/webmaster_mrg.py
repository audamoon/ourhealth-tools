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

    def sitemap_reload(self,i):
        print("Row num: ", i)
        url = self.gs.read_cell("A", True, i)
        url_splited = url.split("//")
        yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/indexing/sitemap/"
        self.gs.write_cell("H", yandex_url, True, i)
        try:
            self.sm.driver.get(yandex_url)
            self.sm.el_by_xpath("//div[@class='tooltip__content'][text()='Отправить файл Sitemap на переобход']")
            btn = self.sm.el_by_xpath("//button[contains(@class,'button_size_xs')]/parent::div")
            btn.click()
            sm.wait_until_presence("//div[@class='tooltip__content'][contains(text(),'Файл был отправлен на переобход')]")
            self.gs.write_cell("G", "Отправлено", True, i)
        except:
            try:
                self.sm.el_by_xpath("//div[@class='tooltip__content'][contains(text(),'Файл был отправлен на переобход')]")
                self.gs.write_cell("G", "Уже было", True, i)
            except:
                self.gs.write_cell("G", "Чета не так", True, i)

    def bypass_counters(self, i):
        print("Row num: ", i)
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
        print("Row num: ", i)
        url = self.gs.read_cell("A", True, i)
        url_splited = url.split("//")
        city_name = self.gs.read_cell("B", True, i)
        print(url,city_name)
        contact_url = url + "/kontakty/"
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

    def collect_sites(self,amount_of_sites):
        pages = (amount_of_sites/20)+1
        links = []
        for page_n in range(1, int(pages)+1):
            self.sm.driver.get(f"https://webmaster.yandex.ru/sites/?page={page_n}")
            sleep(0.5)
            links_el = self.sm.driver.find_elements(By.XPATH,f"//a[@class='Link SitesTableCell-Hostname']")
            for el in links_el:
                links.append(el.text)
        self.gs.write_column_from_array(f"B1:B{len(links)}",links)

    def add_sitemap(self, i):
        print("Row num: ", i)
        url = self.gs.read_cell("A", True, i)
        url_splited = url.split("//")
        sitemap = url + "/sitemaps/"
        yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/indexing/sitemap/"
        self.sm.driver.get(yandex_url)
        self.gs.write_cell("C", yandex_url, True, i)
        try:
            self.sm.wait_until_presence("//input[@name='sitemapUrl']")
            input = self.sm.el_by_xpath("//input[@name='sitemapUrl']")
            input.click()
            input.clear()
            input.send_keys(sitemap)
            self.sm.el_by_xpath("//span[@class='button__text'][text()='Добавить']/parent::button").click()
            self.sm.wait_until_presence("//p[@class='sitemap-files__queue-title'][text()='Очередь на обработку']")
            self.gs.write_cell("B", "Добавлен", True, i)
        except:
            self.gs.write_cell("B", "Чета не так", True, i)


sm = SeleniumManager()
wm = WebmasterManager(sm,"1WsAf_t2PuLD4qowmv5zYyp7YMNpyuSsN0Ir35u5aWQk")
# for el in wm.gs.find_cell_with_word("G","Уже было"):
#     wm.sitemap_reload(el)
#     sleep(1.5)
for cell_num in range(1, 830):
    wm.add_sitemap(cell_num)
    sleep(1.5)
