from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from modules.WMManager import WMManager
from modules.WMElement import Turbo


gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")
driver = ChromeConfigurator.get_driver()
wm = WMManager(driver, gs)

#Доступные параметры для mods в модуле Turbo: add, delete
wm.start(Turbo, ['add'])