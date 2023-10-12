# from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re


class SiteCollector:

    def set_options(self, driver: Chrome, wp_xpath, n_xpath):
        self.driver = driver
        self.wp_xpath = wp_xpath
        self.n_xpath = n_xpath

    def _find_wp(self) -> str:
        if self.wp_xpath == "none":
            return "none"
        wp_element = self.driver.find_element(By.XPATH, self.wp_xpath)
        href = wp_element.get_attribute("href")
        return re.search(r'[+]?[\d]+', href).group(0)

    def _find_number(self) -> list:
        numbers = []
        number_elements = self.driver.find_elements(By.XPATH, self.n_xpath)
        for number_element in number_elements:
            href = number_element.get_attribute("href")
            numbers.append("".join(re.findall(r'[+]?[\d]+', href)))
        return numbers

    def _find_tg(self):
        widget_xpath = "//a[@class='b24-widget-button-social-item ui-icon ui-icon-service-telegram connector-icon-45']"
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, widget_xpath)))
            widget = self.driver.find_element(By.XPATH, widget_xpath)
            href = widget.get_attribute("href")
            return re.search(r'(https://t\.me/)(\w+)', href).group(2)
        except:
            return ""

    def get_data(self, url):
        self.driver.get(url)
        tg = self._find_tg()
        wp = self._find_wp()
        numbers = self._find_number()
        return {"telegram":tg, "wp":wp, "numbers":numbers}