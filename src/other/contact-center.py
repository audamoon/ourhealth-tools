#Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#Google Sheet
from google.oauth2 import service_account
from func.google_sheet_mgr import SheetManager
from apiclient import discovery
#Other
import undetected_chromedriver as uc
from time import sleep
import re

#Подключаю Google Sheet
gs = SheetManager('1Oyk7as5TJ2m339LVSuaqVCDymmCM2ZAcFCurIQhQMSk')

#Настраиваю драйвер
options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Виктор\\AppData\\Local\\Google\\Chrome\\User Data')

#Запускаю драйвер
driver = uc.Chrome(
   browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)

#Функции
def inputLine(site,hello_message,name_of_line):
    #Открываю следующий iframe
    driver.find_element(By.XPATH,"//button[@class='ui-btn ui-btn-link imopenlines-settings-button']").click()
    sleep(3)
    #выхожу из iframe
    driver.switch_to.default_content()
    #выбираю iframe
    driver.switch_to.frame(driver.find_element(By.XPATH,'(//iframe)[3]'))
    #Выбираю отвественного
    driver.find_element(By.XPATH,"//div[@class='ui-tag-selector-tag-remove']").click()
    sleep(1)
    driver.find_element(By.XPATH,"(//span[@class='ui-tag-selector-add-button-caption'])[1]").click()
    sleep(2)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ui-selector-item-title'][text()='Консультант на заявках']")))
    driver.find_element(By.XPATH,"//div[@class='ui-selector-item-title'][text()='Консультант на заявках']").click()
    #Селекты
    select1 = Select(driver.find_element(By.ID, 'imol_operator_data'))
    select1.select_by_value('hide')
    select2 = Select(driver.find_element(By.ID, 'imol_crm_source_select'))
    select2.select_by_visible_text(site)
    #Перехожу в другой отдел меню
    driver.find_element(By.XPATH,"//div[text()='Автоматические действия']/parent::a").click()
    sleep(1)
    driver.find_element(By.XPATH,"(//textarea)[2]").click()
    driver.find_element(By.XPATH,"(//textarea)[2]").clear()
    driver.find_element(By.XPATH,"(//textarea)[2]").send_keys(hello_message)
    #Перехожу в другой отдел меню
    driver.find_element(By.XPATH,"//div[text()='Оценка качества']/parent::a").click()
    sleep(1)
    driver.find_element(By.XPATH,"(//input[@class='imopenlines-control-checkbox'])[17] ").click()
    driver.find_element(By.XPATH,"(//input[@class='imopenlines-control-checkbox'])[16] ").click()
    #Перехожу в другой отдел меню
    driver.find_element(By.XPATH,"//div[text()='Прочее']/parent::a").click()
    sleep(1)
    driver.find_element(By.XPATH,"//input[@name='CONFIG[LINE_NAME]']").click()
    driver.find_element(By.XPATH,"//input[@name='CONFIG[LINE_NAME]']").clear()
    driver.find_element(By.XPATH,"//input[@name='CONFIG[LINE_NAME]']").send_keys(name_of_line)
    sleep(1)
    driver.find_element(By.XPATH,"//button[@class='ui-btn ui-btn-success']").click()
    sleep(3)
    
def ConnectVK (selected_group_name):
    #Переключаюсь на iframe
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH,'(//iframe)[2]'))
    #Нажимаю подключить ВК
    driver.find_element(By.XPATH,"//button[@class='ui-btn ui-btn-lg ui-btn-success ui-btn-round']").click()
    sleep(1)
    #Создаю линк
    oauth_link = driver.find_element(By.XPATH,"//div[@class='ui-btn ui-btn-light-border']").get_attribute('onclick')
    oauth_link = ' '.join(re.findall(r"'([^<>]+)'", oauth_link))
    #Перехожу по ссылке
    driver.execute_script("window.open('','_blank');")
    sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    driver.get(oauth_link)
    checkCaptcha()
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//span[@class='vkuiButton__in']")))
    driver.find_element(By.XPATH,"//span[@class='vkuiButton__in']").click()
    sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    #Переключаюсь на iframe
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH,'(//iframe)[2]'))
    sleep(1)
    #Выбираю нужную группу
    groups = driver.find_elements(By.XPATH,"//div[@class='imconnector-field-social-list-item']")
    for group in groups:
        group_name = group.find_element(By.XPATH, ".//div/div[2]/a").text
        if group_name == selected_group_name:
            connect_group_link = group.find_element(By.XPATH,'./div[2]').get_attribute('onclick')
            connect_group_link = ' '.join(re.findall(r"'([^<>]+)'", connect_group_link))
            #Перехожу по ссылке
            driver.execute_script("window.open('','_blank');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(connect_group_link)
            checkCaptcha()
            WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//button[@class='flat_button fl_r button_indent']")))
            driver.find_element(By.XPATH,"//button[@class='flat_button fl_r button_indent']").click()
            driver.switch_to.window(driver.window_handles[0])
            sleep(2)
            break
def checkCaptcha():
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//form[@class='vkc__Captcha__container vkc__Captcha__adaptive']")))
        while True:
            try:
                a = driver.find_element(By.XPATH,"//form[@class='vkc__Captcha__container vkc__Captcha__adaptive']")
                print(a)
                print('iter')
                sleep(3)
            except:
                break
    except: 
        pass
#Основная программа
for i in range (1,186):
    selected_group_name = gs.readCell(f"A{i}")
    site = gs.readCell(f"C{i}")
    hello_message = gs.readCell(f"D{i}")
    name_of_line = f"VK ▶️ {site} {selected_group_name}"
    driver.get('https://doctor61.bitrix24.ru/contact_center')
    #Захожу на сайт 
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//div[@title='ВКонтакте']")))
    driver.find_element(By.XPATH,"//div[@title='ВКонтакте']").click()
    sleep(3)
    driver.find_element(By.XPATH,f"//div[@id='menu-popup-menuvkgroup']/div/div/div/span[contains(@title,'{selected_group_name}')]").click()
    #driver.find_element(By.XPATH,"//div[@id='menu-popup-menuvkgroup']/div/div/div/span[@title='Создать открытую линию']").click()
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "(//iframe)[2]")))
    #Выбираю iframe
    driver.switch_to.frame(driver.find_element(By.XPATH,'(//iframe)[2]'))
    sleep(1)
    # inputLine(site,hello_message,name_of_line)
    # ConnectVK(selected_group_name)
    # gs.writeCell(f"E{i}",service,sheet_id,"Добавлена")
    try:
        driver.find_element(By.XPATH,"//div[@class='imconnector-field-main-subtitle'][contains(text(),'ВКонтакте подключен')]").click()
        gs.writeCell(f"F{i}","OK")
    except:
        gs.writeCell(f"F{i}","Не ОК")
    
    
#42 119 163 91