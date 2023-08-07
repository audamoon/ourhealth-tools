#Перевести на sheet mgr
import undetected_chromedriver as uc
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from google.oauth2 import service_account
# import google_sheet_func as gs
from apiclient import discovery


def saveRegion(driver, keys, contacts):
    try:
        driver.find_element(
            By.XPATH, "(//input[@class='input__control'])[1]").send_keys(keys)
        sleep(3)
        driver.find_element(
            By.XPATH, "//span[@class='suggest2-item__text'][1]"
        ).click()
        driver.find_element(
            By.XPATH, "(//input[@class='input__control'])[2]").send_keys(contacts)
        sleep(3)
        driver.find_element(
            By.XPATH, ".//span[text()='Сохранить']/parent::button").click()
        sleep(5)
    except:
        driver.refresh()
        WebDriverWait(driver, 6)


scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
sheet_id = '1QzSpvfV_gsCw6NqMN9E9lOmlVCd0DaEwUWF-CCQsuQw'

creds = service_account.Credentials.from_service_account_file(
    'selenium_google_console\service_account_creds.json', scopes=scope
)
service = discovery.build('sheets', 'v4', credentials=creds)

options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument("headless")
driver = uc.Chrome(
   browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options
    )
#driver.set_window_size(1000, 1080)



# with open("selenium_google_console\\scripts\\allsites.txt", "a", encoding='UTF-8') as file1:
#     for i in range(1, 54):
#         driver.get(f"https://webmaster.yandex.ru/sites/?page={i}")
#         sleep(0.5)
#         link_el = driver.find_elements(By.XPATH,f"//a[@class='Link SitesTableCell-Hostname']")
#         for el in link_el:
#             file1.write(f"{el.text} \n")

# for cell_num in range (1060,1062):
#     print("Row num: ", cell_num)
#     url = gs.readCell(f"A{cell_num}",service,sheet_id)
#     url_splited = url.split("//")
#     yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/indexing/crawl-metrika/"
#     gs.writeCell(f"C{cell_num}",service,sheet_id,yandex_url)
#     try:
#         driver.get(yandex_url)
#         driver.find_element(By.XPATH,'//span[text()="Установите на сайт счётчик Яндекс Метрики"]')
#         gs.writeCell(f"B{cell_num}",service,sheet_id,"Не установлена яндекс метрика")
#     except:
#         try:
#             elements = driver.execute_script("let a = document.querySelectorAll('.tumbler__disabled-label');arr = new Array;for (let i = 0; i < a.length; i++) {if (window.getComputedStyle(a[i]).display != 'none'){arr.push(a[i])}};return arr;")
#             if len(elements) != 0:
#                 for el in elements:
#                     el.click()
#                     sleep(1)
#                     gs.writeCell(f"B{cell_num}",service,sheet_id,"Добавлен")
#             else:
#                 gs.writeCell(f"B{cell_num}",service,sheet_id,"Уже был")
#         except:
#             gs.writeCell(f"B{cell_num}",service,sheet_id,"Чета не так")
       

#
# КОД ДЛЯ ДОБАВЛЕНИЯ РЕГИОНОВ В ВЕБМАСТЕРЕ
#

for cell_num in range (859,972):
    print(cell_num)
    url = gs.readCell(f"A{cell_num}",service,sheet_id)
    url_splited = url.split("//")
    city_name = gs.readCell(f"B{cell_num}",service,sheet_id)
    contact_url = url + "/kontakty/" 
    yandex_url = f"https://webmaster.yandex.ru/site/{url_splited[0]}{url_splited[1]}:443/serp-snippets/regions/"
    gs.writeCell(f"D{cell_num}",service,sheet_id,yandex_url)
    try:
        driver.get(yandex_url)
        driver.find_element(By.XPATH, '(//li[@class="regions-list__item"][text()="регион сайта не задан"])[2]')
        driver.find_element(By.XPATH, "(//button)[5]").click()
        driver.find_element(By.XPATH, "(//button)[6]").click()
        saveRegion(driver,city_name,contact_url)
        # WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "(//div[@class='contact_item'])[1]")))
        # city_name = driver.find_element(By.XPATH, "(//div[@class='contact_item'])[1]").text.split(',')[0]
        gs.writeCell(f"C{cell_num}",service,sheet_id,"Добавлен")
    except:
        try:
            driver.find_element(By.XPATH, f"(//li[@class='regions-list__item'][contains(text(),'{city_name}')])")
            gs.writeCell(f"C{cell_num}",service,sheet_id,"Уже был")
            sleep(1)
        except:
            gs.writeCell(f"C{cell_num}",service,sheet_id,"Чета не так")
            sleep(1)

#
#    КОНЕЦ КОДА
#