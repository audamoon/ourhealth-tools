import sys
import undetected_chromedriver as uc
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def createHTML (headers1, header2, headers2, header3, headers3):
    return f"<ul>{headers1} <li><a href='#top2'>{header2}</a></li>{headers2}<li><a href='#top1'>{header3}</a></li> {headers3} </ul>"
    

def inputTextarea(text,btnPath,driver):
    driver.find_element(By.XPATH,f"(//div[@class='cke_inner cke_reset']/span[1]/span[2]/span[1])[{btnPath}]").click()
    driver.find_element(By.XPATH,"//textarea[@dir]").click()
    driver.find_element(By.XPATH,"//textarea[@dir]").clear()
    driver.find_element(By.XPATH,"//textarea[@dir]").send_keys(text)
    driver.find_element(By.XPATH,f"(//div[@class='cke_inner cke_reset']/span[1]/span[2]/span[1])[{btnPath}]").click()

options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument("headless")
driver = uc.Chrome(
    browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
#driver.set_window_size(1000, 1080)


driver.get('https://metod-dovzhenko.com/netcat/admin/#object.list(86746)')
sleep(3)
driver.switch_to.frame('treeIframe')
services_category = driver.find_elements(By.XPATH,"//ul[@id='siteTree_sub-23_children']/li[@class='menu_left_sub']/a")

for category in services_category:
    category.click()
    sleep(1)

services = driver.find_elements(By.XPATH,"//ul[@id='siteTree_sub-23_children']/li/ul/li/a")

for el in services:
    el.click()
    driver.switch_to.default_content()
    sleep(1)

    driver.switch_to.frame('mainViewIframe')
    driver.find_element(By.XPATH,f"(//i[@class='nc-icon nc--edit'])[1]").click()
    driver.switch_to.default_content()
    sleep(1)

    article_content = driver.find_element(By.XPATH,"(//div[@class='nc-field nc-field-type-text'])[2]")
    first_header = False
    first_header_raw = driver.execute_script("return document.querySelector('#f_textBlock1').textContent") 
    second_header = driver.find_element(By.XPATH,"(//div[@class='nc-field nc-field-type-string'])[4]/input").get_attribute('value')
    second_header_text = driver.execute_script("return document.querySelector('#f_textBlock2').textContent") 
    third_header_text = driver.execute_script("return document.querySelector('#f_textBlock3').textContent") 
    third_header = driver.find_element(By.XPATH,"(//div[@class='nc-field nc-field-type-string'])[5]/input").get_attribute('value')
    
    h2_amount = int((first_header_raw.count("h2") + third_header_text.count("h2"))/2 + second_header_text.count("h2")/2)
    li_h1 = ''
    li_h2 = ''
    li_h3 = ''
    header1 = first_header_raw
    header2 = second_header_text
    header3 = third_header_text
    header = ''
    li_el = ''
    for header_id in range (3, h2_amount+3):
            try: 
                header = header1.split("<h2>")[1].split("</h2>")[0]
                li_el = f"<li><a href='#top{header_id}'>{header}</a></li>" 
                li_h1 = li_h1 + li_el
                header1 = header1.replace("<h2>",f"<h2 id='top{header_id}'>",1)
            except:
                try:
                    header = header2.split("<h2>")[1].split("</h2>")[0]
                    li_el = f"<li><a href='#top{header_id}'>{header}</a></li>" 
                    li_h2 = li_h2 + li_el
                    header2 = header2.replace("<h2>",f"<h2 id='top{header_id}'>",1)
                except:
                    try:
                        header = header3.split("<h2>")[1].split("</h2>")[0]
                        li_el = f"<li><a href='#top{header_id}'>{header}</a></li>" 
                        li_h3 = li_h3 + li_el
                        header3 = header3.replace("<h2>",f"<h2 id='top{header_id}'>",1)   
                    except:
                        pass

    inputTextarea(header1,"3",driver)
    inputTextarea(header2,"4",driver)
    header3 = header3.replace("<p>","<p id='top1'>",1)
    inputTextarea(header3,"5",driver)
    
    anchors = createHTML(li_h1,second_header,li_h2,third_header,li_h3)
    inputTextarea(anchors,"2",driver)

#Очистка

    # header1_input = first_header_raw.replace('<h2 id="top3">',"<h2>")
    # header1_input = header1_input.replace('<h2 id="top4">',"<h2>")
    # header1_input = header1_input.replace('<h2 id="top5">',"<h2>")
    # header1_input = header1_input.replace('<h2 id="top6">',"<h2>")
    # header1_input = header1_input.replace('<h2 id="top1">',"<h2>")

    # header2_input = second_header_text.replace('<h2 id="top3">',"<h2>")
    # header2_input = header2_input.replace('<h2 id="top4">',"<h2>")
    # header2_input = header2_input.replace('<h2 id="top5">',"<h2>")
    # header2_input = header2_input.replace('<h2 id="top6">',"<h2>")

    # header3_input = third_header_text.replace('<h2 id="top3">',"<h2>")
    # header3_input = header3_input.replace('<h2 id="top4">',"<h2>")
    # header3_input = header3_input.replace('<h2 id="top5">',"<h2>")
    # header3_input = header3_input.replace('<h2 id="top6">',"<h2>")
    # header3_input = header3_input.replace('<p id="top1">',"<p>")

    # inputTextarea(header1_input,"3",driver)
    # inputTextarea(header2_input,"4",driver)
    # inputTextarea(header3_input,"5",driver)


    driver.find_element(By.XPATH,f"//div[@class='nc-modal-dialog-footer']/button[text()='Сохранить']").click()
    sleep(1.5)
    driver.switch_to.frame('treeIframe')

print('Выполнено')
# driver.switch_to.default_content()//li[@id='siteTree_sub-23']
