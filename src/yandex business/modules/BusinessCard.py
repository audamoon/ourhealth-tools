from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

class PH:
    """Placeholder"""
    VK = "Логин или паблик в ВК"
    OK = "Логин или паблик в Одноклассниках"
    TG = "Логин или канал в Telegram"
    WP = "Номер телефона в WhatsApp"

class BusinessCard:

    order = (PH.VK, PH.OK, PH.WP, PH.TG)

    def __init__(self, driver: Chrome, socials):
        self.driver = driver

    

    def _get_value(self, placeholder, value):
        self.driver.find_element(By.XPATH, f"//input[@placeholder={placeholder}]")

