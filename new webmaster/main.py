from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from WMManager import WMManager
from WMElement import Turbo
from WMTableManager import WMTableManager
import time
gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")

driver = ChromeConfigurator.get_driver()


tm = WMTableManager(driver)

site = 'abaza.neoplus-clinic.ru'
project = "neoplus"
origin_link = "https://webmaster.yandex.ru/site/https:neoplus-clinic.ru:443/turbo/settings/menu/"
subd_link = "https://webmaster.yandex.ru/site/https:abaza.neoplus-clinic.ru:443/turbo/settings/menu/"
driver.get(origin_link)
tm.read_menu_levels("top", project)
tm.read_menu_levels("main", project)
tm.collect_menu_inputs("top", project)
tm.collect_menu_inputs("main", project)
driver.get(subd_link )
tm.create_table("top", project)
tm.input_values_in_menus("top", project, site)
tm.create_table("main", project)
tm.input_values_in_menus("main", project, site)
time.sleep(1000)