from selenium.webdriver.common.by import By
from time import sleep
import re
import os

class NetCatManager:
    iframes = {'left':'treeIframe','center':'mainViewIframe'}
    
    def __init__(self,url,driver) -> None:
        self.url = url
        self.driver = driver
        self.get_main_id()

    def switch_frame(self,view_name):
        if view_name == 'default':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.iframes[view_name])

    def open_netcat(self):
        self.driver.get(self.url)

    def open_subtitles(self,subs):
        for sub in subs:
            sub.click()
            sleep(1)

    def get_main_id(self):
        main_link = self.url
        self.main_id = "".join(re.findall(r'([^()]+)', main_link)[1])

class Subtitle:

    def __init__(self, subtitle_url,subtitle_name) -> None:
        self.url = subtitle_url
        self.name = subtitle_name

class SubtitleFactory:

    def makeSubtitle(subtitle_url,subtitle_name):
        return Subtitle(subtitle_url=subtitle_url, subtitle_name=subtitle_name)

class NetCatFunctions:
    def __init__(self, netcat_mgr,selenium_mgr) -> None:
        self.nm = netcat_mgr
        self.sm = selenium_mgr

    def choose_file_path(self,path):
        self.folder_path = path

    def open_subs(self,xpath=""):
        """Открывает видимые разделы

        Дополнительно можно указать XPATH, крайней элемент должен быть li
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")
        if xpath == "":
            xpath = f"//img[@alt='Раскрыть список']"
        else:
            xpath = xpath + f"/img[@alt='Раскрыть список']"
        print(xpath)
        print(self.sm.els_by_xpath(xpath))
        self.nm.open_subtitles(self.sm.els_by_xpath(xpath))

    def write_active_subs(self):
        """Позволяет записать активные разделы в файл
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")
        
        with open(self.folder_path + "/temp/subtitles.txt","w", encoding="UTF-8") as subtitles_file:
            subs = self.sm.els_by_xpath("//a[@class='menu_left_a active']")
            for sub in subs:
                subtitles_file.write(sub.get_attribute('title') + "\n")
                
    def choose_subs(self):
        """Перезаписывает файл, оставляя в нём только выбранные разделы
        """
        choosed_subs = input("Введите выбранные разделы через пробел: ")
        choosed_subs = choosed_subs.split(" ")
        with open(self.folder_path + "/temp/subtitles.txt","r", encoding="UTF-8") as subtitles_file:
            subs = subtitles_file.readlines()
        with open(self.folder_path + "/temp/subtitles.txt","w", encoding="UTF-8") as subtitles_file:
            for choosed_sub in choosed_subs:
                for sub in subs:
                    if choosed_sub in sub:
                        subtitles_file.write(sub) 

    def get_URl(self):
        """Записывает в файл URL выбранных разделов.

        Важное условие: выбранные разделы должны быть видимыми
        """
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")

        with open(os.getcwd() + "/temp/subtitles.txt","r",encoding="UTF-8") as subtitles_file:
            choosed_subs = subtitles_file.readlines()
            for i in range (len(choosed_subs)):
                choosed_subs[i] = choosed_subs[i].replace("\n","")

        subs = self.sm.els_by_xpath("//a[@class='menu_left_a active']")

        with open(os.getcwd() + "/temp/subtitles.txt","w",encoding="UTF-8") as subtitles_file:
            for choosed_sub in choosed_subs:
                for sub in subs:
                    title = sub.get_attribute('title')
                    if choosed_sub in title:
                        sub.click()
                        subtitles_file.write(title + f";{self.sm.driver.current_url}" + "\n")

    def get_sub_children(self):
        self.nm.switch_frame("default")
        self.nm.switch_frame("left")
        """Находит детей выбранных разделов и записывает их в файл
        """
        with open(os.getcwd() + "/temp/subtitles.txt","r",encoding="UTF-8") as subtitles_file:
            choosed_subs = subtitles_file.readlines()
        for i in range (len(choosed_subs)):
            choosed_subs[i] = choosed_subs[i].replace("\n","")

        with open(os.getcwd() + "/temp/subtitles.txt","w",encoding="UTF-8") as subtitles_file:
            for choosed_sub in choosed_subs:
                choosed_sub_el = self.sm.el_by_xpath(f"//a[@title='{choosed_sub}']")
                choosed_sub_el.click()
                sleep(1)
                # subtitles_file.write(choosed_sub + "\n")
                self.open_subs(f"//a[@title='{choosed_sub}']/parent::li/ul/li/")
                sub_children = self.sm.els_by_xpath(f"//a[@title='{choosed_sub}']/parent::li/ul/li/a[@class='menu_left_a active']")
                for sub_child in sub_children:
                    title = sub_child.get_attribute('title')
                    subtitles_file.write(title + "\n")

            