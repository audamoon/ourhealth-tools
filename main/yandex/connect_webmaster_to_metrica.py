import sys
import undetected_chromedriver as uc
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

options = uc.ChromeOptions()
options.add_argument(
    '--user-data-dir=C:\\Users\\Sergey\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument("headless")
driver = uc.Chrome(
    browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
#driver.set_window_size(1000, 1080)
id = "66051736"
driver.get(f"https://metrika.yandex.ru/settings?id={id}")
sleep(5)
def ConnectWebMaster(driver):
    length = len(driver.find_elements(By.XPATH, ".//span[text()='Привязать к Вебмастеру']/parent::button"))
    for i in range(1, length):
        scroll_vаlue = 500
        scroll_by = f'window.scrollBy(0, {scroll_vаlue});'
        try:
            driver.execute_script(scroll_by)
            driver.find_element(By.XPATH,f"(.//span[text()='Привязать к Вебмастеру']/parent::button)[{i}]").click()
            i += 1
        except:
            ConnectWebMaster(driver)
            
ConnectWebMaster(driver)
