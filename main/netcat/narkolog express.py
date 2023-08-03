#Перевести на sheet mgr
import undetected_chromedriver as uc
# import google_sheet_func as gs
# import captcha as captcha
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apiclient import discovery
from google.oauth2 import service_account
from selenium.webdriver.common.action_chains import ActionChains


def chooseCorrectArray (category):
    advantagesArrayDefault = {"Медицинская лицензия":"/netcat_template/template/redizain/banners/licence.svg",
                   "Опытные доктора":"/netcat_template/template/redizain/banners/doctor and benzol.svg"
                   ,"Проверенные лекарства":"/netcat_template/template/redizain/banners/hand holds pill.svg",
                   "Полная анонимность":"/netcat_template/template/redizain/banners/question mark face.svg"}

    advantagesArrayDrugs = {"Медицинская лицензия":"/netcat_template/template/redizain/banners/licence.svg",
                    "Справедливая цена":"/netcat_template/template/redizain/banners/hand holds scales.svg"
                    ,"Проверенные лекарства":"/netcat_template/template/redizain/banners/double drugs.svg",
                    "Полная анонимность":"/netcat_template/template/redizain/banners/question mark face.svg"}

    advantagesArrayAlcohol = {"Медицинская лицензия":"/netcat_template/template/redizain/banners/licence.svg",
                    "Качественное оборудование":"/netcat_template/template/redizain/banners/dropper.svg"
                    ,"Проверенные лекарства":"/netcat_template/template/redizain/banners/medkit.svg",
                    "Полная анонимность":"/netcat_template/template/redizain/banners/question mark face.svg"}

    advantagesArrayPsyco = {"Медицинская лицензия":"/netcat_template/template/redizain/banners/licence.svg",
                    "Опытные доктора":"/netcat_template/template/redizain/banners/doctor and benzol.svg"
                    ,"Внимание к проблеме":"/netcat_template/template/redizain/banners/mental breakdown.svg",
                    "Полная анонимность":"/netcat_template/template/redizain/banners/question mark face.svg"}
    
    allAdvantages = [advantagesArrayDefault,advantagesArrayAlcohol,advantagesArrayDrugs,advantagesArrayPsyco]

    key = 0
    match category:  
        case '19.': 
            key = 1
        case '16.':
            key = 2
        case '152466.':
            key = 3
        case _:
            key = 0
    return allAdvantages[key]
    


def keysChoose(input_id,driver,array):
    result = ""
    values = list(array.values())
    keys = list(array.keys())
    alt = driver.find_element(By.XPATH,f"//h2[1]").text
    match input_id:
        case 4:
            result = alt
        case 7:
            result = keys[0]
        case 8:
            result = values[0]
        case 9:
            result = keys[1]
        case 10:
            result = values[1]
        case 11:
            result = keys[2]
        case 12:
            result = values[2]
        case 13:
            result = keys[3]
        case 14:
            result = values[3]
        case _:
            pass
    return result


options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument("headless")
driver = uc.Chrome(
    browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
#driver.set_window_size(1000, 1080)

serviceCategoryList = ["21.","17.","20.","18.","16.","19.","152466."]
serviceList = [
# ["59","58","56","57","60","61","62","63","64","65","66","67","68","144035","171758","189705","189706","189707","189708","189709","189710","189711","189712"],#21
# ["46","144033","171748"],#17
# ["69"],#20
# ["47","49","48","51","50","52","53","54","171749","171755"],#18
# ["35","40","41","37","38","42","39","43","144031","171747","171753"],#16
#["70","71","72","73","74","75","76","77","78","79","80","81","82",
[
    #"83","85","86","87","88","89",
    "171750"]
    #,#19
#["152467","152468","152470","152472","152473","152474","152475","152476","152477","171752"],#152466
]

for i in range (0,len(serviceList)):
    for j in range (0,len(serviceList[i])):
        serviceList[i][j]  = serviceList[i][j]  + '.'

driver.get('https://narkolog.express/netcat/admin/#object.list(11)')
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "treeIframe")))
sleep(5)

for i in range (0, len(serviceCategoryList)):
    serviceCategoryId = serviceCategoryList[i]
    driver.switch_to.frame('treeIframe')
    driver.find_element(By.XPATH,f"//span[@class='node_id'][text()='{serviceCategoryId}']").click()
    driver.switch_to.default_content()
    sleep(5)
    driver.switch_to.frame('mainViewIframe')
    driver.find_element(By.XPATH,f"(//i[@class='nc-icon nc--edit'])[1]").click()
    driver.switch_to.default_content()
    sleep(2)
    input_array = [4,7,8,9,10,11,12,13,14]
    for input_id in input_array:
        driver.find_element(By.XPATH,f"(//div[@class='nc-field nc-field-type-string']/input)[{input_id}]").clear()
        driver.find_element(By.XPATH,f"(//div[@class='nc-field nc-field-type-string']/input)[{input_id}]").click()
        driver.find_element(By.XPATH,f"(//div[@class='nc-field nc-field-type-string']/input)[{input_id}]").send_keys(
            keysChoose(input_id,driver,chooseCorrectArray(serviceCategoryId)))
        
    driver.find_element(By.XPATH,f"//div[@class='nc-modal-dialog-footer']/button[text()='Сохранить']").click()
    sleep(7)
    # for j in range (0, len(serviceList[i])):
    #     driver.switch_to.frame('treeIframe')
    #     driver.find_element(By.XPATH,f"//span[@class='node_id'][text()='{serviceList[i][j]}']").click()
    #     sleep(4)
    #     driver.switch_to.default_content()
    #     driver.switch_to.frame('mainViewIframe')
    #     driver.find_element(By.XPATH,f"(//i[@class='nc-icon nc--edit'])[1]").click()
    #     driver.switch_to.default_content()
    #     sleep(2)

        
