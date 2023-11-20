from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from WMmanager import WMmanager
from WMElement import Turbo
gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")
driver = ChromeConfigurator.get_driver()
wm = WMmanager(driver, gs)
print("hello")
# wm.collect_sites(100)
wm.mod_launch(Turbo, "delete")