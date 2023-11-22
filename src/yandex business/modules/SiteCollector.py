# from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re


class SiteCollector:

    def set_options(self, driver: Chrome):
        self.driver = driver

    def _find_href(self, xpath):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element = self.driver.find_element(By.XPATH, xpath)
            href = element.get_attribute("href")
        except:
            href = "Null"
        return href

    def _find_numbers(self) -> list:
        number_xpath = '//a[starts-with(@href, "tel:")]'
        numbers = []
        number_elements = self.driver.find_elements(By.XPATH, number_xpath)
        for number_element in number_elements:
            href = number_element.get_attribute("href")
            numbers.append("".join(re.findall(r'[+]?[\d]+', href)))
        return list(set(numbers))

    def _find_tg(self):
        widget_xpath = "//a[@class='b24-widget-button-social-item ui-icon ui-icon-service-telegram connector-icon-45']"
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, widget_xpath)))
            widget = self.driver.find_element(By.XPATH, widget_xpath)
            href = widget.get_attribute("href")
            return re.search(r'(https://t\.me/)(\w+)', href).group(2)
        except:
            return "Null"

    def get_data(self, url):
        VK_XPATH = "(//a[contains(@href,'vk.com')])[1]"
        OK_XPATH = "(//a[contains(@href,'ok.ru')])[1]"
        WP_XPATH = "//a[contains(@href,'whatsapp.com') or contains(@href, 'wa.me')]"
        self.driver.get(url)

        numbers = self._find_numbers()
        vk = self._find_href(VK_XPATH)
        ok = self._find_href(OK_XPATH)
        try:
            wp = re.search(r'[+]?[\d]+', self._find_href(WP_XPATH)).group(0)
        except:
            wp = "Null"
        tg = self._find_tg()

        return {"numbers": numbers, "vk": vk, "ok": ok, "wp": wp, "telegram": tg}