import undetected_chromedriver as uc
import os
from gseleniumconf.profiles import ProfileID


class ChromeConfigurator():

    def __init__(self, profile_id: ProfileID):
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

    def get_driver(profile_id: ProfileID = ProfileID.DEFAULT):
        """
        return Chrome class

        Usage:
        1) ChromeConfigurator.get_driver()
        2) ChromeConfigurator.get_driver(ProfileID.FIRST)

        second option need if you want use another but not default Chrome profile

        """
        return ChromeConfigurator(profile_id).__driver