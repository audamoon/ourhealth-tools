from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class PH:
    """Placeholder"""
    VK = "Логин или паблик в ВК"
    OK = "Логин или паблик в Одноклассниках"
    WP = "Номер телефона в WhatsApp"
    TG = "Логин или канал в Telegram"
   

class BusinessCard:

    order = (PH.VK, PH.OK, PH.WP, PH.TG)

    def __init__(self, driver: Chrome, socials, numbers):
        self.driver = driver
        self.socials = socials
        self.numbers = numbers

    def __scroll_page(self):
        action = ActionChains(self.driver)
        action.scroll_to_element(self.driver.find_element(By.XPATH, "//div[text()='Территория оказания услуг']")).perform()

    def compare_values(self):
        self.__scroll_page()
        table_values = self.socials
        
        for i in range(len(self.order)):
            target = self.driver.find_element(By.XPATH, f"//input[@placeholder='{self.order[i]}']")
            value = target.get_attribute("value")
            if value != table_values[i]:
                target.click()
                target.clear()
                target.send_keys(table_values[i])


                