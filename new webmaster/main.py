from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from WMmanager import WMmanager

gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")
# driver = ChromeConfigurator.get_driver()
driver = ''
wm = WMmanager(driver, gs)
wm.launch()
