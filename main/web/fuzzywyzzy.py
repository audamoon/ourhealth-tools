from fuzzywuzzy import fuzz
import sys
import undetected_chromedriver as uc
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class ServiceHandler:
    array = []
    def ShowArray(self):
        print(self.array)
    def CreateArray(self,item):
        self.array = item
    def ClearArray(self):
        for i in range (len(self.array)):
            self.array[i] = self.array[i].replace("\n","")
            self.array[i] = self.array[i].replace("\ufeff","")
            self.array[i] = self.array[i].lower()

services = ServiceHandler()
links = ServiceHandler()

with open("main/web/services.txt", "r", encoding='UTF-8') as file1:
    read_content = file1.readlines()
    services.CreateArray(read_content)

with open("main/web/links.txt", "r", encoding='UTF-8') as file2:
    read_content = file2.readlines()
    links.CreateArray(read_content)

links.ClearArray()
services.ClearArray()

givenOpt = services.array

options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument("headless")
driver = uc.Chrome(
    browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
#driver.set_window_size(1000, 1080)

for link in links.array:
    with open ("main/web/result.txt","a", encoding="UTF-8") as f_result:
        f_result.write('='*50 + "\n")
        f_result.write('    '*3 + "РЕЗУЛЬТАТ ПАРСИНГА САЙТА" + "\n")
        f_result.write('='*50 + "\n")
        f_result.write(link + "\n")
        f_result.write('='*50 + "\n")

    driver.get(link)
    sleep(2)

    text_containers = driver.execute_script("return document.querySelectorAll('.narkolog-suptitle')")
    # text_containers = driver.find_elements(By.XPATH, "//p")
    #.narkolog-suptitle .text-section__container 

    text_str = ''

    for block in text_containers:
        text_str += block.text
    text_str = text_str.split('.')

    for sequence in text_str:
        for service in givenOpt:
            ratio = fuzz.WRatio(sequence.lower(),service)
            if ratio >= 87:
                with open ("main/web/result.txt","a", encoding="UTF-8") as f_result:
                    f_result.write(f"Элемент [{sequence.strip()}] \n")
                    f_result.write(f"Совпадение по слову \"{service}\" - {ratio}%\n")
                    
    with open ("main/web/result.txt","a", encoding="UTF-8") as f_result:
        f_result.write('='*50 + "\n")
        f_result.write("\n")
        f_result.write("\n")