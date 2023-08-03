#Перевести на sheet mgr
import undetected_chromedriver as uc
# import google_sheet_func as gs
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apiclient import discovery
from google.oauth2 import service_account
from selenium.webdriver.common.action_chains import ActionChains
# Авторизация Google Sheet
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
sheet_id = '16kKsrGuM9a9LlbKXCMNBrJba5kCGusLYySgCmntjc9E'

creds = service_account.Credentials.from_service_account_file(
    'service_account_creds.json', scopes=scope
)
service = discovery.build('sheets', 'v4', credentials=creds)

options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument("headless")
driver = uc.Chrome(
    browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
#driver.set_window_size(1000, 1080)

for i in range (2,104):
    try:
        link = gs.readCell(f"Яндекс.Организации!C{i}", service, sheet_id)
        driver.get(link)
        sleep(1)
        driver.find_element(By.XPATH,"//div[@class='VerificationCheck VerificationCheck_size_l CompanyEditHeader-Verified']")
        gs.writeCell(f"Яндекс.Организации!F{i}", service, sheet_id, 'Подтверждено')
        sleep(0.5)
    except:
        gs.writeCell(f"Яндекс.Организации!F{i}", service, sheet_id, 'Подтверждается')
        sleep(1)

# for i in range (98, 99):
#     cellNumber = i
#     citySiteCell = gs.readCell(f"Яндекс.Организации!B{cellNumber}", service, sheet_id)
#     addressSiteCell = gs.readCell(f"Яндекс.Организации!C{cellNumber}", service, sheet_id)
#     statusCell = gs.readCell(f"Яндекс.Организации!D{cellNumber}", service, sheet_id)

#     if (citySiteCell != "Такой сраницы нет") and (statusCell != "уже была") and (statusCell != "Заполнено"): 
#         cityName = citySiteCell.split(".")[0].split("://")[1]
#         email = cityName + "@narkology.pro"
#         ok = "https://ok.ru/group/70000000264266"
#         vk = "https://vk.com/narkologypro"
#         tg = "https://t.me/narkologypro_bot"
#         whatsapp = "+79952227421"
#         number = "88005517014"
#         businessAddress = addressSiteCell[:-5]
#         driver.get(businessAddress)
#         sleep(3)
#         socials_array = {5:vk,9:ok,12:tg,13:whatsapp,17:email}
#         for key in socials_array:
#             driver.find_element(By.XPATH,f"(//INPUT[@class='input__control i-bem input__control_js_inited'])[{key}]").click()
#             driver.find_element(By.XPATH,f"(//INPUT[@class='input__control i-bem input__control_js_inited'])[{key}]").send_keys(socials_array[key])
#         #add phone
#         driver.find_element(By.XPATH,"(//SPAN[@class='icon icon_serp_trash-outline-neoblue-light-16 plural-collection__icon i-bem'])[2]").click()
#         driver.find_element(By.XPATH,"(//INPUT[@class='input__control i-bem input__control_js_inited'])[14]").click()
#         driver.find_element(By.XPATH,"(//INPUT[@class='input__control i-bem input__control_js_inited'])[14]").send_keys(number)
#         sleep(0.3)
#         #save
        
#         driver.find_element(By.XPATH,"//button[@class='button button_theme_islands button_size_l button_view_action button_type_submit page-edit-company__submit page-edit-company__submit_type_save page-edit__submit metrika button__control i-bem page-edit-company__submit_js_inited button_js_inited button__control_js_inited']").click()
#         #WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='notification notification_theme_success notification_icons i-bem notification_js_inited notification_activated']")))
#         sleep(3)
        
#         driver.get(businessAddress + "/features")
#         sleep(3)
#         for i in range (0,15):
#                 scroll_vаlue = 150
#                 scroll_by = f"window.scrollBy(0, {scroll_vаlue});" 
#                 driver.execute_script(scroll_by)
#         checkbox_id = [1,2,12,13,15,16,9,27,47,60,63,65,61]

#         for id in checkbox_id:
#             element = ''
#             if id == 27:
#                 element = driver.find_element(By.XPATH,f"(//span[@class='button__text'])[{id}]")
#                 actions = ActionChains(driver)
#                 actions.move_to_element(element)
#                 actions.perform()
#                 element.click()
#             else:
#                 element = driver.find_element(By.XPATH,f"(//span[@class='checkbox__box'])[{id}]")
#                 actions = ActionChains(driver)
#                 actions.move_to_element(element)
#                 actions.perform()
#                 element.click()
            
#         button_id = [21,24,28,32,43]
#         for id in button_id:
#             element = driver.find_element(By.XPATH,f"(//span[@class='button__text'])[{id}]")
#             actions = ActionChains(driver)
#             actions.move_to_element(element)
#             actions.perform()
#             element.click()
#         sleep(0.3)
#         driver.find_element(By.XPATH,"//button[@class='button button_theme_islands button_size_l button_view_action button_type_submit page-edit-features__submit page-edit__submit metrika button__control i-bem page-edit-features__submit_js_inited button_js_inited button__control_js_inited']").click()
#         #WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='notification notification_theme_success notification_icons i-bem notification_js_inited notification_activated']")))
#         sleep(3)
#         gs.writeCell(f"Яндекс.Организации!D{cellNumber}", service, sheet_id, 'Заполнено')
#     else: 
#         pass
