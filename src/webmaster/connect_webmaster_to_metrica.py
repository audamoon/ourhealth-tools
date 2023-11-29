import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from gseleniumconf.chrome import ChromeConfigurator


def ClickButtons(driver:uc.Chrome, path_to_button):
    buttons = driver.find_elements(By.XPATH, path_to_button)
    length = len(buttons)
    action = ActionChains(driver)
    for i in range(length):
            target = buttons[i]
            action.scroll_to_element(target).perform()
            target.click()
    sleep(5)

driver = ChromeConfigurator.get_driver()

id = "87033584"
driver.get(f"https://metrika.yandex.ru/settings?id={id}")
sleep(1)
driver.execute_script('document.querySelector(".counter-edit__counter-buttons.counter-edit__counter-buttons_show_yes").remove()')

connect = ".//span[text()='Привязать к Вебмастеру']/parent::button"
back = "//span[text()='Отменить']/parent::button"
reconnect = "//span[text()='Отправить запрос ещё раз']/parent::button"
ClickButtons(driver, connect)
# ClickButtons(driver, back)
# ClickButtons(driver, reconnect)
driver.quit()
