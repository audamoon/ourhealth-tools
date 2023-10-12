from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from func.selenium_mgr import SeleniumManager
from func.google_sheet_mgr import SheetManager

from time import sleep


def enter_input(input,key):
    input.click()
    input.clear()
    input.send_keys(key)

def add_phone(phone_id, phone):
    add_phone = driver.find_element(By.XPATH,f"//span[text()='Добавить номер']")
    add_phone.click()
    phone_form = driver.find_element(By.XPATH,f"(//input[@placeholder='Номер телефона'])[{phone_id}]")
    enter_input(phone_form, phone)


driver = SeleniumManager().driver
actions = ActionChains(driver)
gs = SheetManager("1bbU7BPXn6PpebVbqbLQiR_qKRBUZ-tEqxLv5fmDAX3Y")



def set_general(edit_link):
    #=================Основные====================
    driver.get(edit_link)
    driver.refresh()

    #Вставляем поля
    inputs_array = {"круглосуточно":"Введите в формате «Пн-Пт 9:00-18:00»","narcolog.express":"Логин или паблик в ВК","group/57474318663799":"Логин или паблик в Одноклассниках",
                    "narkolog_express_bot":"Логин или канал в Telegram","info@narkolog.express":"Адрес электронной почты"}

    for key in inputs_array:
        value = inputs_array[key]
        input_element = driver.find_element(By.XPATH,f"//input[@placeholder='{value}']")
        enter_input(input_element,key)
        print(value)

    #Телефон
    hide_phone = driver.find_element(By.XPATH,"//span[text()='Скрыть']")
    hide_phone.click()
    add_phone(2,"8 (800) 707-82-93")
    add_phone(3,"8 (961) 407-09-30")

    #Название 
    add_name = driver.find_element(By.XPATH,f"//span[text()='Добавить название']")
    add_name.click()
    sleep(0.5)
    choose_btn = driver.find_element(By.XPATH,"//div[contains(@data-bem,'На английском')]")
    choose_btn.click()
    sleep(0.5)
    name_input = driver.find_element(By.XPATH,f"(//input[@placeholder='Полное'])[2]") 
    enter_input(name_input, 'Narcolog Express')
    sleep(0.8)
    #Сохраняем
    save_btn = driver.find_element(By.XPATH,"//span[text()='Сохранить данные']")
    save_btn.click() 
    sleep(1.5)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='notification notification_theme_success notification_icons i-bem notification_js_inited notification_activated']")))
    
def set_features(features_link):
    #=================Особенности====================
    driver.get(features_link)
    sleep(2)
    #Показать всё
    show_more_btn = driver.find_element(By.XPATH, "//button[@class='button button_theme_islands button_size_m show-more__more button__control i-bem']")
    show_more_btn.click()

    #Чекбоксы
    checkbox_num = [1,2,9,12,13,14,15,48,61,62,64,66]
    for num in checkbox_num:
        btn = driver.find_element(By.XPATH, f"(//span[@class='checkbox__box'])[{num}]")
        btn.click()
        sleep(0.1)

    #Кнопки
    toggle_num = [1,5,7,19,22,25,28,32,43]
    for num in toggle_num:
        toggle_btn = driver.find_element(By.XPATH, f"(//button[contains(@class,'button_togglable_radio')]/span)[{num}]")
        toggle_btn.click()
        sleep(0.1)

    #Сохраняем  
    driver.find_element(By.XPATH,"//span[text()='Сохранить данные']").click()
    sleep(1.5)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='notification notification_theme_success notification_icons i-bem notification_js_inited notification_activated']")))

def complete_cards(edit_link, features_link):
    try:
        set_general(edit_link)
        # set_features(features_link)
        return "Заполнена"
    except:
        return "Фейл"


for row_num in range(1,6):
    status = gs.read_cell("C",True,row_num)
    if status != "Заполнена":
        edit_link = gs.read_cell("A",True,row_num)
        features_link = gs.read_cell("B",True,row_num)
        result = complete_cards(edit_link, features_link)
        gs.write_cell("C", result, True, row_num)
        sleep(1)