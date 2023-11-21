from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from WMManager import WMManager
from WMElement import Turbo
from WMTableManager import WMTableManager

gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")

driver = ChromeConfigurator.get_driver()

wm = WMManager(driver, gs)

wm.mod_launch(Turbo, ["add"])




# driver.get("https://webmaster.yandex.ru/site/https:neoplus-clinic.ru:443/turbo/settings/menu/")

# tm = WMTableManager(driver)

# site = 'arkhangelsk.neoplus-clinic.ru'
# project = "neoplus"
# origin_link = "https://webmaster.yandex.ru/site/https:neoplus-clinic.ru:443/turbo/settings/menu/"
# tm.input_values_in_menus("top", project, site)
# wm = WMManager(driver, gs)
