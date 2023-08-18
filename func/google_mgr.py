from func.google_sheet_mgr import SheetManager
from func.selenium_mgr import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class GoogleManager:
    def __init__(self,driver) -> None:
        self.driver = driver

    def add_sitemap(self,gs, i):
        site = gs.read_cell("B",True,i)
        sitemap = gs.read_cell("E",True,i)
        try:
            self.driver.get('https://search.google.com/u/1/search-console/welcome')
            self.driver.find_element(
                By.XPATH, '//input[@aria-label="https://www.example.com"]').send_keys(site)
            sleep(3)
            self.driver.find_element(
                By.XPATH, "(//SPAN[@class='RveJvd snByac'][text()='Продолжить'])[2]").click()
            sleep(3)
            self.driver.find_element(
                By.XPATH, "(//SPAN[@class='RveJvd snByac'][text()='Перейти к ресурсу'])[2]").click()
            sleep(3)
            self.driver.find_element(
                By.XPATH, "//SPAN[contains(text(),'Файлы Sitemap')]/div[@class='d1pwUc']").click()
            sleep(3)
            self.driver.find_element(
                By.XPATH, "(//INPUT[@type='text'])[4]").send_keys(sitemap)
            sleep(3)
            self.driver.find_element(
                By.XPATH, "//SPAN[@class='RveJvd snByac'][text()='Отправить']").click()
            sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//DIV[@id='dwrFZd1']")))
            gs.write_cell("G","Добавлен",True,i)
        except:
            gs.write_cell("G","Что-то пошло не так",True,i)
        

        
gs = SheetManager("1qvQJs_BKM4-C9hMOsqIl8lrC7pAbr96Adh3K9KATyGs")
sm = SeleniumManager()
gm = GoogleManager(sm.driver)
for el in gs.find_cell_with_word("G","Что-то пошло не так"):
    gm.add_sitemap(gs,el)