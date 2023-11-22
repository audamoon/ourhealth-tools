from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from modules.WMManager import WMManager
from modules.WMElement import Counter, Region

#11eXl_6VOHuYljBQbTt6A29-SBS3EvyGaPTw7gjotRYY - новая таблица
gs = SheetManager("11eXl_6VOHuYljBQbTt6A29-SBS3EvyGaPTw7gjotRYY")
driver = ChromeConfigurator.get_driver()
wm = WMManager(driver, gs)

wm.start(Region, ["add"])

# data_origin = "https://webmaster.yandex.ru/site/https:neoplus-clinic.ru:443/turbo/settings/menu/"
# wm.getMenu(data_origin, 'top', "neoplus-clinic.ru")
# wm.getMenu(data_origin, 'main', 'neoplus-clinic.ru')
# wm.start(TurboMenu, ["top", "main"])
# wm.saveResult("logs\\result2023-11-22-16-25.txt")