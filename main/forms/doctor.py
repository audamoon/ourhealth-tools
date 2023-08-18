from func.selenium_mgr import SeleniumManager
from selenium.webdriver.common.by import By
from time import sleep
import json
import random
import string
def generate_phone_number():
    region_code = "950"
    phone_number = "+7 ({}) {}{}{}-{}{}-{}{}".format(
        region_code,
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9)
    )
    return phone_number

def enter_input(input,keys):
    input.clear()
    input.click()
    input.send_keys(keys)

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.sample(letters, length))
    return rand_string

with open("main/forms/sites.json","r",encoding="UTF-8") as jsonfile:
    data = json.load(jsonfile)
    sites = data["sites"]
    id = data["id"]
    numbers = data["phones"]

site_number = data["id"]
data["id"] += 1
print(f"№{str(site_number)}/{len(sites)} | сайт: {sites[site_number]}")
sm = SeleniumManager()
sm.driver.get(sites[site_number])
name = "Тестовая форма"

phone = generate_phone_number()
email = "test_form@mail.ru"
message = "Отправил тестовую форму"

######################################################
sm.driver.find_element(By.XPATH,'//a[@href="#consult"]').click()
enter_input(sm.driver.find_element(By.XPATH,"//form[@id='consult']/input[@name='f_name']"),name)
enter_input(sm.driver.find_element(By.XPATH,"//form[@id='consult']/input[@name='f_phone']"),phone)
enter_input(sm.driver.find_element(By.XPATH,"//form[@id='consult']/input[@name='f_email']"),email)
enter_input(sm.driver.find_element(By.XPATH,"//form[@id='consult']/textarea[@name='f_message']"),message)

sm.driver.find_element(By.XPATH,"//form[@id='consult']/button[@type='submit']").click()
sm.wait_until_presence("//button[@class='mfp-close']")
sm.driver.find_element(By.XPATH,"//button[@class='mfp-close']").click()

#####################################################
sm.driver.find_element(By.XPATH,'//a[@href="#callback"]').click()
phone = generate_phone_number()


enter_input(sm.driver.find_element(By.XPATH,"//form[@id='callback']/input[@name='f_phone']"),phone)

sm.driver.find_element(By.XPATH,"//form[@id='callback']/button[@type='submit']").click()
sm.wait_until_presence("//button[@class='mfp-close']")
sm.driver.find_element(By.XPATH,"//button[@class='mfp-close']").click()

##################################################
phone = generate_phone_number()

enter_input(sm.driver.find_element(By.XPATH,"//input[@class='promo__form-input'][@name='f_name']"),name)
enter_input(sm.driver.find_element(By.XPATH,"//input[@class='promo__form-input'][@name='f_phone']"),phone)

sm.driver.find_element(By.XPATH,"//input[@class='promo__form-btn']").click()
sm.wait_until_presence("//button[@class='mfp-close']")
sm.driver.find_element(By.XPATH,"//button[@class='mfp-close']").click()



################################
try:
    sm.wait_until_presence("//div[@data-b24-crm-button-icon='openline']") 
    sm.driver.find_element(By.XPATH,"//div[@data-b24-crm-button-icon='openline']").click()
    sm.driver.find_element(By.XPATH,"//a[@class='b24-widget-button-social-item b24-widget-button-openline_livechat']").click()

    sm.wait_until_presence("//textarea[@class='bx-im-textarea-input']")
    enter_input(sm.driver.find_element(By.XPATH,"//textarea[@class='bx-im-textarea-input']"),message)
    sm.wait_until_presence("//button[@class='bx-im-textarea-send-button bx-im-textarea-send-button-bright-arrow']")
    sm.driver.find_element(By.XPATH,"//button[@class='bx-im-textarea-send-button bx-im-textarea-send-button-bright-arrow']").click()
    sm.wait_until_presence("(//input[@class='b24-form-control'][@name='name'])[2]")
    "(//div[@class='b24-form'])[2]"
    arr = ["tester","testovik","testesteron","tesg","gegewh","hreheh",""]
    sleep(1)
    str1 = generate_random_string(random.randint(4,8))
    str2 = generate_random_string(random.randint(4,8))
    tel = str(random.randint(111111,99999999))
    test_mail = f"test_form{random.randint(10,1000)}@gmail.com"
    enter_input(sm.driver.find_element(By.XPATH,"(//div[@class='b24-form'])[2]//input[@class='b24-form-control'][@name='name']"),str1)
    enter_input(sm.driver.find_element(By.XPATH,"(//div[@class='b24-form'])[2]//input[@class='b24-form-control'][@name='lastname']"),str2)
    enter_input(sm.driver.find_element(By.XPATH,"(//div[@class='b24-form'])[2]//input[@class='b24-form-control'][@name='phone']"),tel)
    enter_input(sm.driver.find_element(By.XPATH,"(//div[@class='b24-form'])[2]//input[@class='b24-form-control'][@name='email']"),test_mail)
    print(str1,str2,tel,test_mail)
    
    
    sleep(1)
    sm.driver.find_element(By.XPATH,"(//button[@class='b24-form-btn'])[2]").click()
    sleep(5)

    with open("main/forms/done.txt","a",encoding="UTF-8") as file:
        file.write(sites[site_number] + "\n")
except:
    with open("main/forms/error.txt","a",encoding="UTF-8") as file:
        file.write(sites[site_number] + "\n")

with open("main/forms/sites.json","w",encoding="UTF-8") as jsonfile:
    json.dump(data,jsonfile,ensure_ascii=False)