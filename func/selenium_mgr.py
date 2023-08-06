from abc import ABC, abstractmethod
#Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#Other
import undetected_chromedriver as uc
import os

class SeleniumProfile(ABC):

    @abstractmethod
    def create_driver(self):
        pass

class SeleniumChromeProfile(SeleniumProfile):

    user_path = (os.environ['LOCALAPPDATA'] + "\\Google\\Chrome\\User Data")
    def create_driver(self):
        super().create_driver()
        self.options = uc.ChromeOptions()
        self.options.add_argument(f"--user-data-dir={self.user_path}")
        self.driver = uc.Chrome(
            browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=self.options)
        
    def get_driver(self):
        return self.driver
        
class SeleniumManager:

    def __init__(self,driver_type="google") -> None:
        """driver_type - передаёт тип драйвера (gecko,google, etc).

        По умолчанию driver_type="google"
        """
        self.choose_driver(driver_type)

    def choose_driver(self,driver_type):
        match driver_type.lower():
            case "google":
                driver_object = SeleniumChromeProfile()
                driver_object.create_driver()
                self.driver = driver_object.get_driver()
            case _:
                print("Select driver type")

    def wait_until_presence(self,xpath,time=600):
        """Сокращённая запись WebDriverWait

        По умолчанию time=600
        """
        WebDriverWait(self.driver,time).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def el_by_xpath(self,xpath):
        """Сокращённая запись find_element
        """
        return self.driver.find_element(By.XPATH,xpath)
    
    def els_by_xpath(self,xpath):
        """Сокращённая запись find_elements
        """
        return self.driver.find_elements(By.XPATH,xpath)
        
