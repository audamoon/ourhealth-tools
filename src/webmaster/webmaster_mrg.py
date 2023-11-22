from func.google_sheet_mgr import SheetManager
from func.selenium_mgr import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class WebmasterManager:
    def __init__(self, driver: SeleniumManager, sheet_id) -> None:
        self.sm = driver
        self.gs = SheetManager(sheet_id)

    # def input_values_to_table(self, row_id, names, domens):
    #     inputs = self.sm.driver.find_elements(
    #         By.XPATH, "//div[@class='turbo-setup-menu__main']//input")
    #     # ссылки четные, имена - нечетные
    #     city_link = self.gs.read_cell(f"B{row_id}")

    #     links = []
    #     for domen in domens:
    #         links.append(city_link + domen[0])
    #     for i in range(len(inputs)//2):
    #         # all numbers reversed
    #         input_even_number = 2 * i + 1
    #         inputs[input_even_number].click()
    #         inputs[input_even_number].clear()
    #         inputs[input_even_number].send_keys(links[i])
    #         input_odd_number = 2 * i
    #         inputs[input_odd_number].click()
    #         inputs[input_odd_number].clear()
    #         inputs[input_odd_number].send_keys(names[i])

    #     save_btn = self.sm.driver.find_element(
    #         By.XPATH, "button button_size_m button_theme_action button_align_left form__submit form__submit_align_left i-bem")
    #     save_btn.click()

    # def create_table(self):
    #     self.sm.driver.get(
    #         "https://webmaster.yandex.ru/site/https:spb.alco.rehab:443/turbo/settings/menu/")

    #     sleep(2)

    #     add_lvl_1_btn = self.sm.driver.find_element(
    #         By.XPATH, "//button[@class='button button_size_s button_menu-level_1 button_theme_normal sun-table__turbo-setup-menu-add i-bem']")

    #     for i in range(3):
    #         add_lvl_1_btn.click()
    #     sleep(1)

    #     for n in range(3):

    #         amount_of_lvl_2 = [8, 15, 5]
    #         amount_of_lvl_3 = [[1, 11], [2], []]
    #         numbers_lvl_3 = [[1, 2], [2], []]
    #         lvl_1 = self.sm.driver.find_element(
    #             By.XPATH, f"//tr[@class='sun-table__row sun-table__row_menu-level_1'][{n+1}]")
    #         lvl_1.find_element(By.XPATH, f"./td[2]/span").click()
    #         add_lvl_2_btn = lvl_1.find_element(
    #             By.XPATH, ".//button[@class='button button_size_s button_menu-level_2 button_theme_normal sun-table__turbo-setup-menu-add i-bem']")

    #         for j in range(amount_of_lvl_2[n]-1):
    #             add_lvl_2_btn.click()

    #         expand_lvl_3_btns = lvl_1.find_elements(
    #             By.XPATH, f".//span[@class='link link_pseudo_yes link_theme_normal link_menu-level_2 sun-table__turbo-setup-submenu-add i-bem']")

    #         for el in numbers_lvl_3[n]:
    #             if len(numbers_lvl_3) == 0:
    #                 break
    #             expand_lvl_3_btns[el].click()

    #         add_lvl_3_btns = lvl_1.find_elements(
    #             By.XPATH, ".//button[@class='button button_size_s button_menu-level_3 button_theme_normal sun-table__turbo-setup-menu-add i-bem']")

    #         for k in range(len(numbers_lvl_3[n])):
    #             print(f"n = {n}, k = {k}")
    #             for lvl3_num in range(amount_of_lvl_3[n][k]-1):
    #                 add_lvl_3_btns[k].click()

    def sitemap_reload(self, row_num):
        self.__open_url(row_num, "A", "C", "/indexing/sitemap/")
        try:
            self.sm.el_by_xpath(
                "//div[@class='tooltip__content'][text()='Отправить файл Sitemap на переобход']")
            btn = self.sm.el_by_xpath(
                "//button[contains(@class,'button_size_xs')]/parent::div")
            btn.click()
            sm.wait_until_presence(
                "//div[@class='tooltip__content'][contains(text(),'Файл был отправлен на переобход')]")
            return 'Отправлено'
        except:
            try:
                self.sm.el_by_xpath(
                    "//div[@class='tooltip__content'][contains(text(),'Файл был отправлен на переобход')]")
                return 'Было'
            except:
                return "Чета не так"

    # def bypass_counters(self, row_num):
    #     self.__open_url(row_num, "A", "E", "/indexing/crawl-metrika/")
    #     try:
    #         self.sm.driver.find_element(
    #             By.XPATH, '//span[text()="Установите на сайт счётчик Яндекс Метрики"]')
    #         return "Не установлена яндекс метрика"
    #     except:
    #         try:
    #             elements = self.sm.driver.execute_script(
    #                 "let a = document.querySelectorAll('.tumbler__disabled-label');arr = new Array;for (let i = 0; i < a.length; i++) {if (window.getComputedStyle(a[i]).display != 'none'){arr.push(a[i])}};return arr;")
    #             if len(elements) != 0:
    #                 for el in elements:
    #                     el.click()
    #                     sleep(1)
    #                     return "Добавлен"
    #             else:
    #                 return "Уже был"
    #         except:
    #             return "Ошибка"

    # def add_region(self, row_num):
    #     self.__open_url(row_num, "B", "F", "/serp-snippets/regions/")
    #     city_name = self.gs.read_cell("A", True, row_num)
    #     contact_url = self.gs.read_cell("C", True, row_num)
    #     try:
    #         self.sm.el_by_xpath(
    #             '(//li[@class="RegionsList-Item"]/*[text()="регион сайта не задан"])[2]')
    #         self.sm.el_by_xpath(
    #             "//button[contains(@class,'RegionsPage-PlusButton')]").click()
    #         self.sm.wait_until_presence(
    #             "//span[text()='Добавить регион']/parent::span/parent::button", 5)
    #         self.sm.el_by_xpath(
    #             "//span[text()='Добавить регион']/parent::span/parent::button").click()
    #         self.saveRegion(city_name, contact_url)
    #         return "Добавлен"
    #     except:
    #         try:
    #             self.sm.el_by_xpath(
    #                 f"(//li[@class='RegionsList-Item']/*[contains(text(),'{city_name}')])")
    #             return "Уже был"
    #         except:
    #             return "Ошибка"

    # def saveRegion(self, keys, contacts):
    #     try:
    #         inputRegionXPATH = "(//input[@class='yc-text-input__control yc-text-input__control_type_input'])[3]"
    #         self.sm.wait_until_presence(inputRegionXPATH, 5)
    #         self.sm.el_by_xpath(inputRegionXPATH).click()
    #         self.sm.el_by_xpath(inputRegionXPATH).send_keys(keys)
    #         sleep(1)
    #         self.sm.el_by_xpath(
    #             "//div[@class='RegionSuggest-Item'][1]").click()
    #         self.sm.el_by_xpath(
    #             "//input[@class='yc-text-input__control yc-text-input__control_type_input'][@type='url']").send_keys(contacts)
    #         sleep(1)
    #         self.sm.el_by_xpath(
    #             "//span[text()='Сохранить']/parent::span/parent::button").click()
    #         sleep(3)
    #     except:
    #         self.sm.driver.refresh()
    #         sleep(3)

    # def collect_sites(self, amount_of_sites):
    #     pages = (amount_of_sites/20)+1
    #     links = []
    #     for page_n in range(1, int(pages)+1):
    #         self.sm.driver.get(
    #             f"https://webmaster.yandex.ru/sites/?page={page_n}")
    #         sleep(0.5)
    #         links_el = self.sm.driver.find_elements(
    #             By.XPATH, f"//a[@class='Link SitesTableCell-Hostname']")
    #         for el in links_el:
    #             links.append(el.text)
    #     self.gs.write_column_from_array(f"A1:A{len(links)}", links)

    def delete_sitemap(self):
        self.sm.wait_until_presence("//button[@aria-label='Удалить']", 1)
        self.sm.el_by_xpath("//button[@aria-label='Удалить']").click()

    def add_sitemap(self, row_num):
        self.__open_url(row_num, "B", "E", "/indexing/sitemap/")
        sitemap = self.gs.read_cell("C", True, row_num)
        try:
            # try:
            #     self.delete_sitemap()
            # except:
            #     pass
            self.sm.wait_until_presence("//input[@name='sitemapUrl']")
            input = self.sm.el_by_xpath("//input[@name='sitemapUrl']")
            input.click()
            input.clear()
            input.send_keys(sitemap)
            self.sm.el_by_xpath(
                "//span[@class='button__text'][text()='Добавить']/parent::button").click()
            self.sm.wait_until_presence(
                "//p[@class='sitemap-files__queue-title'][text()='Очередь на обработку']")
            return "Добавлен"
        except:
            return "Ошибка"

    # def __open_url(self, row_num, get_link_col, write_link_col, add_subfolder):
    #     print("Row num: ", row_num)
    #     url = self.gs.read_cell(get_link_col, True, row_num)
    #     url_splited = url.split("//")
    #     print(url_splited)
    #     yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443{add_subfolder}"
    #     self.sm.driver.get(yandex_url)
    #     self.gs.write_cell(write_link_col, yandex_url, True, row_num)

    # def add_turbo(self, row_num):
    #     self.__open_url(row_num, "A", "D", "/turbo/sources")
    #     turbo = self.gs.read_cell("B", True, row_num)
    #     try:
    #         self.sm.el_by_xpath("//div[contains(text(),'вам не принадлежит')]")
    #         return "не принадлежит"
    #     except:
    #         self.delete_turbo()
    #         try:
    #             self.sm.wait_until_presence("//input[@name='feedUrl']")
    #             self.sm.el_by_xpath("//input[@name='feedUrl']").click()
    #             self.sm.el_by_xpath("//input[@name='feedUrl']").clear()
    #             self.sm.el_by_xpath(
    #                 "//input[@name='feedUrl']").send_keys(turbo)
    #             self.sm.el_by_xpath(
    #                 "//button[@class='button button_side_right button_theme_action button_align_left button_size_m one-line-submit__submit form__submit i-bem button_js_inited']").click()
    #             # self.sm.wait_until_presence("//td[text()='Без ошибок']")

    #             WebDriverWait(self.sm.driver, 60).until(EC.element_to_be_clickable(
    #                 (By.XPATH, "//div[text()='Откл']/parent::div")))
    #             self.sm.el_by_xpath("//div[text()='Откл']/parent::div").click()

    #             try:
    #                 self.sm.wait_until_presence(
    #                     "//button[@class='button button_theme_action button_size_s confirm__confirm i-bem button_js_inited']", 5)
    #                 # вот ниже если мы делаем с удалить турбо на надо 2-ю по счету искать п отому что это пидорас создает второе окошко
    #                 self.sm.el_by_xpath(
    #                     "(//button[@class='button button_theme_action button_size_s confirm__confirm i-bem button_js_inited'])[1]").click()
    #                 self.sm.wait_until_presence(
    #                     "//td[text()='Проверяется']", 3)
    #                 return "Проверяется"
    #             except:
    #                 self.sm.wait_until_presence(
    #                     "//td[text()='Проверяется']", 3)
    #                 return "Проверяется"
    #         except:
    #             return "Что-то не так"

    # def check_turbo(self, row_num):
    #     self.__open_url(row_num, "A", "D", "/turbo/sources")
    #     try:
    #         # sm.driver.find_element(By.XPATH, '//button[contains(@class,"button_delete_yes")]').click()
    #         # sleep(0.5)
    #         # sm.driver.find_element(By.XPATH, '//button[contains(@class,"confirm__confirm")]').click()
    #         # sleep(0.1)
    #         # sm.driver.find_element(By.XPATH, "//td[@class='turbo-source__type luna-table__cell']")
    #         sm.driver.find_element(
    #             By.XPATH, "//button[contains(@class,'tumbler__button')][@aria-pressed='false']").click()
    #         self.sm.wait_until_presence(
    #             "//button[@class='button button_theme_action button_size_s confirm__confirm i-bem button_js_inited']", 1)
    #         self.sm.el_by_xpath(
    #             "//button[@class='button button_theme_action button_size_s confirm__confirm i-bem button_js_inited']").click()
    #         return "Удалил"
    #     except:
    #         return "Не удалил"

    # def add_metrika(self, row_num):
    #     self.__open_url(row_num, "A", "C", "/settings/metrika/")
    #     sleep(0.5)
    #     try:
    #         self.sm.driver.find_element(
    #             By.XPATH, "//*[text()='Связан с сайтом в Вебмастере']")
    #         return "Был"
    #     except:
    #         try:
    #             btn_path = "//span[text()='Подтвердить']/parent::button"
    #             self.sm.driver.find_element(By.XPATH, btn_path).click()
    #             self.sm.wait_until_presence(
    #                 "//*[text()='Связан с сайтом в Вебмастере']")
    #             return "Добавлен"
    #         except:
    #             return "Ошибка"

    # def save_load(self, row_num, status_array, range_letter="B"):
    #     if len(status_array) == 10:
    #         self.gs.write_column_from_array(
    #             f"{range_letter}{row_num-9}:{row_num + len(status_array)}", status_array)
    #     if len(status_array) < 10:
    #         self.gs.write_column_from_array(
    #             f"{range_letter}{row_num-len(status_array)+1}:{row_num}", status_array)

    # def delete_turbo(self):
    #     print("начинаю удоление")
    #     deleteBtns = self.sm.driver.find_elements(
    #         By.XPATH, "//button[@class='button button_delete_yes button_only-icon_yes button_theme_clear button_size_s luna-table__delete turbo-source__delete i-bem']")
    #     for deletebtn in deleteBtns:
    #         deletebtn.click()
    #         sleep(2)
    #         self.sm.driver.find_element(
    #             By.XPATH, "//span[text()='Удалить']/parent::button").click()
    #         sleep(1)


# sm = SeleniumManager()
# wm = WebmasterManager(sm, "1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")

# wm.collect_sites(1076)
# exit()
# min_range = 11
# max_range = 1412
# status_array = []
# for row_num in range(min_range, max_range):
#     status_array.append(wm.add_region(row_num))
#     if row_num % 10 == 0:
#         wm.save_load(row_num, status_array, "D")
#         status_array = []
#     if max_range - row_num == 1:
#         wm.save_load(row_num, status_array, "D")
#         status_array = []


# names = wm.gs.get_values("B")
# for name in names:
#     sm.driver.get(f"https://webmaster.yandex.ru/site/{name[0]}:443/dashboard/")


# domens = wm.gs.get_values("D")
# for row_id in range(37,97):
#     wm.add_turbo(row_id)

# sleep(100)
# max_range = 76
# status_array = []

# for row_num in range(2,max_range):
#     status_array.append(wm.add_sitemap(row_num))
#     if row_num % 10 == 0:
#         wm.save_load(row_num,status_array,"C")
#         status_array = []
#     if max_range - row_num == 1:
#             wm.save_load(row_num,status_array,"C")
#             status_array = []

# Для отладки
# for row_num in wm.gs.find_cell_with_word("F","не принадлежит","ТУРБО"):
#     wm.add_turbo(row_num)
#     sleep(5)
