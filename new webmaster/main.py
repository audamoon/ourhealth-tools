from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from WMManager import WMManager
from WMElement import TurboMenu

gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")
driver = ChromeConfigurator.get_driver()
wm = WMManager(driver, gs)


data_origin = "https://webmaster.yandex.ru/site/https:neoplus-clinic.ru:443/turbo/settings/menu/"

wm.start(TurboMenu, ["top", "main"])
# wm.getMenu(data_origin, 'top')
# wm.getMenu(data_origin, 'main')
