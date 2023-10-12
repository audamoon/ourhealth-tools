from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
import time

driver = ChromeConfigurator.get_driver()
driver.get("https://metrika.yandex.ru/settings?id=64744489&tab=common")
all_domens = []
list_items = driver.find_elements(By.XPATH, "//div[contains(@class,'counter-mirrors-list-item form-fields i-bem form-fields_js_inited counter-mirrors-list-item_js_inited')]")
print("start working")
for list_item in list_items:
    try: 
        message = list_item.find_element(By.XPATH, ".//div[text()='Ждет подтверждения в Вебмастере']")
        value = list_item.find_element(By.XPATH, ".//input[@placeholder='Домен или путь (без http, https и www)']").get_attribute("value")
        all_domens.append(value + "\n")
    except:
        continue
print("done")
driver.quit()
with open("webmaster/parsers/unactive_domens.txt", "a" ,encoding="UTF-8") as result_file:
    result_file.writelines(all_domens)