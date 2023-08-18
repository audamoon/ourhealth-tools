#Перевести на sheet mgr
import undetected_chromedriver as uc
from time import sleep
# import scripts.google_sheet_func as gs
# import scripts.captcha as captcha
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apiclient import discovery
from google.oauth2 import service_account


def YandexLogin(login, password, driver):
    driver.find_element(
        By.XPATH, "(.//span[text()='Почта']/parent::button)[1]").click()
    sleep(3)
    driver.find_element(By.XPATH, "//input[@name='login']").send_keys(login_ya)
    driver.find_element(By.XPATH, "//button[@id='passp:sign-in']").click()
    sleep(3)
    driver.find_element(
        By.XPATH, "//input[@id='passp-field-passwd']").send_keys(pass_ya)
    driver.find_element(By.XPATH, "//button[@id='passp:sign-in']").click()
    captcha.FindTrouble(driver, "//h1[contains(text(),'form')]")
    sleep(5)


def saveRegion(driver, keys, contacts):
    try:
        driver.find_element(
            By.XPATH, "(//input[@class='input__control'])[1]").send_keys(keys)
        sleep(3)
        driver.find_element(
            By.XPATH, "(//div[@data-bem])[11]"
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


def addShitToPage(driver, keys, contacts,i):
    try:
        driver.find_element(
            By.XPATH, ".//span[text()='Добавить регион']/parent::button").click()
        saveRegion(driver, keys, contacts)
        gs.writeCell(f"B{i}", service, sheet_id, '1')
    except:
        saveRegion(driver, keys, contacts)
        gs.writeCell(f"B{i}", service, sheet_id, '1')


def WebMasterReg(driver, end_point):
    for i in range(28, end_point):
        keys = "Челябинская область"
        contacts = gs.readCell(f"D{i}", service, sheet_id)
        address = gs.readCell(f"A{i}", service, sheet_id)
        driver.get('https://webmaster.yandex.ru/site/' +
                   address + "/serp-snippets/regions/")
        sleep(3)
        try:
            YandexLogin(login_ya, pass_ya, driver)
            driver.find_element(By.XPATH,"(//button)[3]").click()
            addShitToPage(driver, keys, contacts,i)
        except:
            driver.find_element(By.XPATH,"(//button)[3]").click()
            addShitToPage(driver, keys, contacts,i)


scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
sheet_id = '18pWqbjtDu06CwFASwyQ8KUcf_68HipiW3ZnCZE1R6AA'
creds = service_account.Credentials.from_service_account_file(
    'service_account_creds.json', scopes=scope
)
service = discovery.build('sheets', 'v4', credentials=creds)


options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
options.add_argument("headless")
driver = uc.Chrome(
    browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
driver.set_window_size(1000, 1080)

login_ya = 'doctor.zapoy@yandex.ru'
pass_ya = 'k)M-Xjs3i$'


WebMasterReg(driver, 36)
