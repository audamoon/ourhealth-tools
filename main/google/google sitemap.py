import undetected_chromedriver as uc
import scripts.google_sheet_func as gs
import scripts.captcha as captcha
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apiclient import discovery
from google.oauth2 import service_account


# Авторизация Google Sheet
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
sheet_id = '1qvQJs_BKM4-C9hMOsqIl8lrC7pAbr96Adh3K9KATyGs'

creds = service_account.Credentials.from_service_account_file(
    'service_account_creds.json', scopes=scope
)

# Запуск сервисов
service = discovery.build('sheets', 'v4', credentials=creds)
options = uc.ChromeOptions()
#options.add_argument("headless")
driver = uc.Chrome(options=options)

driver.get('https://www.ligastavok.ru/?utm_referrer=https%3A%2F%2Fyandex.ru%2F')
sleep(6)
print(driver.find_element(By.XPATH,"//div[@class='bui-scores__total-2da964']").text)

# Учетные данные
username_google = 'pohmelochnaya@gmail.com'
password_google = 'Ns-fDC![05'
username_netcat = 'mizevvln@yandex.ru'
password_netcat = "PD%cp_KXIV4V"

# Вход google


def loginGoogle(username, password, driver):
        driver.get('https://accounts.google.com/ServiceLogin')
        sleep(2)

        driver.find_element(
            By.XPATH, '//input[@type="email"]').send_keys(username)
        driver.find_element(By.XPATH, '//*[@id="identifierNext"]').click()
        sleep(2)

        driver.find_element(
            By.XPATH, '//input[@type="password"]').send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="passwordNext"]').click()
        sleep(2)

        captcha.FindTrouble(
            driver, '//span[text()="Подтвердите свою личность"]')

# Добавления sitemap


def AddSiteMap(site, sitemap):
    try:
        driver.get('https://search.google.com/u/1/search-console/welcome')
        sleep(2)
        driver.find_element(
            By.XPATH, '//input[@aria-label="https://www.example.com"]').send_keys(site)
        driver.find_element(
            By.XPATH, "(//SPAN[@class='RveJvd snByac'][text()='Продолжить'])[2]").click()
        sleep(5)
        driver.find_element(
            By.XPATH, "(//SPAN[@class='RveJvd snByac'][text()='Перейти к ресурсу'])[2]").click()
        sleep(2)
        driver.find_element(
            By.XPATH, "//SPAN[contains(text(),'Файлы Sitemap')]/div[@class='d1pwUc']").click()
        sleep(2)
        driver.find_element(
            By.XPATH, "(//INPUT[@type='text'])[4]").send_keys(sitemap)
        sleep(2)
        driver.find_element(
            By.XPATH, "//SPAN[@class='RveJvd snByac'][text()='Отправить']").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//DIV[@id='dwrFZd1']")))
        return True

    except:
        print('Найдена ошибка с добавлением в сайтмап, пытаюсь устранить')
        AddSiteMap(site, sitemap)


# Вход в NetCat
def loginNetcat(username, password, driver):
    driver.get('https://pohmelochnaya.ru/netcat/admin/#index')
    sleep(2)
    driver.find_element(
        By.XPATH, '//input[@name="AUTH_USER"]').send_keys(username)
    driver.find_element(
        By.XPATH, '//input[@name="AUTH_PW"]').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()


# Проверка наличия гугл тега
def checkGoogleMeta(driver, city_name):
    driver.get('https://pohmelochnaya.ru/netcat/admin/#index')
    sleep(5)
    driver.switch_to.frame(driver.find_element(By.ID, 'treeIframe'))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, f"//a[contains(text(),'{city_name}')]")))
    driver.find_element(
        By.XPATH, f"//a[contains(text(),'{city_name}')]").click()
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//SPAN[text()='Настройки']")))
    driver.find_element(
        By.XPATH, "//SPAN[text()='Настройки']").click()
    sleep(3)
    driver.find_element(
        By.XPATH, "//LI[@class='button'][text()='Дополнительные настройки']").click()
    driver.switch_to.frame(driver.find_element(By.ID, 'mainViewIframe'))
    try:
        driver.find_element(By.XPATH, "//textarea[contains(text(),'google')]")
        return True
    except:
        return False


# def getRange(range, i):
#     return f"Гугл серч консоль!{range}{i}"


# loginGoogle(username_google,password_google,driver)
# loginNetcat(username_netcat,password_netcat,driver)

# for i in range(1, 123):
#     try:
#         rangeA = getRange('A', i)
#         rangeB = getRange('B', i)
#         rangeC = getRange('C', i)
#         rangeD = getRange('D', i)
#         rangeE = getRange('E', i)
#         rangeF = getRange('F', i)
#         site = gs.readCell(range=rangeB, service=service, sheet_id=sheet_id)
#         sitemap = "sitemap/" + site.split('://')[1][:-1] + ".xml"
#         sitemap_full_link = sitemap_full_link = site + \
#             "sitemap/" + site.split('://')[1][:-1] + ".xml"
#         city_name = gs.readCell(
#             range=rangeA, service=service, sheet_id=sheet_id)
#         # Проверяем консоль
#         if gs.readCell(range=rangeD, service=service, sheet_id=sheet_id) == '0':
#             if checkGoogleMeta(driver=driver, city_name=city_name) == True:
#                 gs.writeCell(range=rangeD, service=service,
#                              sheet_id=sheet_id, value='1')
#             else:
#                 gs.writeCell(range=rangeD, service=service,
#                              sheet_id=sheet_id, value='0')
#         # Проверяем гугл
#         if gs.readCell(range=rangeE, service=service, sheet_id=sheet_id) == '0':

#             if AddSiteMap(site, sitemap) == True:
#                 gs.writeCell(range=rangeE, service=service,
#                              sheet_id=sheet_id, value='1')
#                 gs.writeCell(range=rangeC, service=service,
#                              sheet_id=sheet_id, value=sitemap_full_link)
#             else:
#                 gs.writeCell(range=rangeE, service=service,
#                              sheet_id=sheet_id, value='0')
#     except:
#         gs.writeCell(rangeF, service, sheet_id,
#                      'Возникла ошибка')
#         continue
