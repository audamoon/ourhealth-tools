from typing import Any
import undetected_chromedriver as uc
import os

class Profile:
    def __init__(self, name):
        self.name = name

class ProfileID:
    FIRST = Profile("").name
    SECOND = Profile("Profile 2").name
    THIRD = Profile("Profile 3").name
    FORTH = Profile("Profile 4").name

    def get_ids(self):
        return [self.FIRST, self.SECOND,self.THIRD, self.FORTH]

class ChromeConfigurator():
    #"C:\Users\Sergey\AppData\Local\Google\Chrome\User Data\Profile 1    \Google\Chrome\User Data\Profile 1\Default"

    def __init__(self, profile_id:ProfileID = ProfileID.FIRST):
        self.__user_path = (os.environ['LOCALAPPDATA'] + f"\\Google\\Chrome\\User Data")
        self.__profile_directory = (f"{profile_id}")
        self.__set_driver()


    def __set_driver(self):
        self.__options = uc.ChromeOptions()
        self.__options.add_argument(f"--user-data-dir={self.__user_path}")
        self.__options.add_argument(f"--profile-directory={self.__profile_directory}")
        self.__driver = uc.Chrome(
            browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",
            options=self.__options)

    def get_driver(self):
        return self.__driver
    