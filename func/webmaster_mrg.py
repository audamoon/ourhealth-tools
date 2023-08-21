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

    def bypass_counters(self, row_num):
        self.__open_url(row_num,"A","E","/indexing/crawl-metrika/")
        # print("Row num: ", row_num)
        # url = self.gs.read_cell("A", True, row_num)
        # url_splited = url.split("//")
        # yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/indexing/crawl-metrika/"
        # self.gs.write_cell("D", yandex_url, True, row_num)
        try:
            self.sm.driver.find_element(By.XPATH,'//span[text()="Установите на сайт счётчик Яндекс Метрики"]')
            return "Не установлена яндекс метрика"
        except:
            try:
                elements = self.sm.driver.execute_script("let a = document.querySelectorAll('.tumbler__disabled-label');arr = new Array;for (let i = 0; i < a.length; i++) {if (window.getComputedStyle(a[i]).display != 'none'){arr.push(a[i])}};return arr;")
                if len(elements) != 0:
                    for el in elements:
                        el.click()
                        sleep(1)
                        return "Добавлен"
                        self.gs.write_cell("E", "Добавлен", True, i)
                else:
                    return "Уже был"
                    self.gs.write_cell("E", "Уже был", True, i)
            except:
                return "Ошибка"
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
            # for el in links_el:
            #     links.append(el.text)
            for el in links_el:
                if ".clinic" in el.text:
                    links.append(el.text)
        self.gs.write_column_from_array(f"A1:A{len(links)}",links)

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
    
    def __open_url(self,row_num,get_link_col,write_link_col,add_subfolder):
        print("Row num: ", row_num)
        url = self.gs.read_cell(get_link_col, True, row_num)
        url_splited = url.split("//")
        print(url_splited)
        yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443{add_subfolder}"
        self.sm.driver.get(yandex_url)
        self.gs.write_cell(write_link_col, yandex_url, True, row_num)
    
    def add_turbo(self,row_num):
        self.__open_url(row_num,"ТУРБО!B","ТУРБО!H","/turbo/sources/")
        turbo = self.gs.read_cell("ТУРБО!D", True, row_num)
        try: 
            self.sm.el_by_xpath("//div[contains(text(),'вам не принадлежит')]")
            self.gs.write_cell("ТУРБО!F", "не принадлежит", True, row_num)
        except:
            try:  
                self.sm.wait_until_presence("//input[@name='feedUrl']")

                self.sm.el_by_xpath("//input[@name='feedUrl']").click()
                self.sm.el_by_xpath("//input[@name='feedUrl']").clear()
                self.sm.el_by_xpath("//input[@name='feedUrl']").send_keys(turbo)

                self.sm.el_by_xpath("//button[@class='button button_side_right button_theme_action button_align_left button_size_m one-line-submit__submit form__submit i-bem button_js_inited']").click()
                
                self.sm.wait_until_presence("//td[text()='Без ошибок']")
                self.sm.el_by_xpath("//div[text()='Откл']/parent::div").click()
                try:
                    self.sm.wait_until_presence("//button[@class='button button_theme_action button_size_s confirm__confirm i-bem button_js_inited']",5)
                    self.sm.el_by_xpath("//button[@class='button button_theme_action button_size_s confirm__confirm i-bem button_js_inited']").click()
                    self.sm.wait_until_presence("//td[text()='Проверяется']")
                    self.gs.write_cell("ТУРБО!F", "Проверяется", True, row_num)
                except:
                    self.sm.wait_until_presence("//td[text()='Проверяется']")
                    self.gs.write_cell("ТУРБО!F", "Проверяется", True, row_num)
            except:
                self.gs.write_cell("ТУРБО!F", "Что-то не так", True, row_num)

    def add_metrika(self,row_num):
        self.__open_url(row_num, "A", "C", "/settings/metrika/")
        sleep(0.5)
        try:
            self.sm.driver.find_element(By.XPATH,"//*[text()='Связан с сайтом в Вебмастере']")
            return "Был"
        except:
            try:
                btn_path = "//span[text()='Подтвердить']/parent::button"
                self.sm.driver.find_element(By.XPATH,btn_path).click()
                self.sm.wait_until_presence("//*[text()='Связан с сайтом в Вебмастере']")
                return "Добавлен"
            except:
                return "Ошибка"    

    def save_load(self,row_num,status_array,range_letter="B"): 
        if len(status_array) == 10:
            self.gs.write_column_from_array(f"{range_letter}{row_num-9}:{row_num + len(status_array)}", status_array)
        if len(status_array) < 10:
            self.gs.write_column_from_array(f"{range_letter}{row_num-len(status_array)+1}:{row_num}", status_array)
            

sm = SeleniumManager()
wm = WebmasterManager(sm,"1h_FM0dD7IxgHMMa1WIe_OQtDSRJtoirUg4PfVjj_XHI")

max_range = 1268
status_array = []

for row_num in range(1,max_range):
    status_array.append(wm.bypass_counters(row_num))
    if row_num % 10 == 0:
        wm.save_load(row_num,status_array,"D")
        status_array = []
    if max_range - row_num == 1:
            wm.save_load(row_num,status_array,"D")
            status_array = []

#Для отладки
# for row_num in wm.gs.find_cell_with_word("F","не принадлежит","ТУРБО"):
#     wm.add_turbo(row_num)
#     sleep(5)