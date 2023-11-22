import undetected_chromedriver as uc
import os


class ChromeConfigurator:

    @staticmethod
    def get_driver(profile_id = ""):
        """
        return Chrome class

        Usage:
        1) ChromeConfigurator.get_driver()
        2) ChromeConfigurator.get_driver(ProfileID.FIRST)

        second option need if you want use another but not default Chrome profile

        """
        user_path = os.environ['LOCALAPPDATA'] + f"\\Google\\Chrome\\User Data"
        profile_directory = f"{profile_id}"
        
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_path}")
        options.add_argument(f"--profile-directory={profile_directory}")

        driver = uc.Chrome(
            browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",
            options=options)
        
        return driver