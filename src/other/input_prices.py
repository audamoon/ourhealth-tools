from func.configurator import ChromeConfigurator
import json
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("prices.json", "r", encoding="UTF-8") as file:
    prices = json.load(file)

driver = ChromeConfigurator().get_driver()



for i in range(len(prices)):
    name = prices[f"price-{i}"][0]
    price = prices[f"price-{i}"][1]
    driver.get("https://triumf.center/netcat/admin/#object.list(117880)")
    sleep(2)
    driver.execute_script("nc.load_dialog('/netcat/add.php?inside_admin=1&cc=117880')")
    # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='save']")))
    # driver.find_element(By.XPATH, "//div[@class='save']").click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='nc_capfld_428']/parent::div/input")))
    name_el = driver.find_element(By.XPATH, "//span[@id='nc_capfld_428']/parent::div/input")
    price_el = driver.find_element(By.XPATH, "//span[@id='nc_capfld_429']/parent::div/input")
    name_el.click()
    name_el.clear()
    name_el.send_keys(name)

    price_el.click()
    price_el.clear()
    price_el.send_keys(price)
    driver.find_element(By.XPATH, "//button[@data-action='submit']").click()
    sleep(4)
