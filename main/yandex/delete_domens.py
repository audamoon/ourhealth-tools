from func.google_sheet_mgr import SheetManager
from func.selenium_mgr import SeleniumManager
from selenium.webdriver.common.by import By
from time import sleep

SheetManager("1WsAf_t2PuLD4qowmv5zYyp7YMNpyuSsN0Ir35u5aWQk")
sm = SeleniumManager()
for i in range(2,1123):
    sm.driver.get(f"https://webmaster.yandex.ru/sites/?page=2")
    el = sm.el_by_xpath("(//tbody/tr/td/span[@class='I18N'])[1]")
    el.find_element(By.XPATH,"./parent::td/parent::tr/td//div[@class='Delete']/div").click()
    sm.el_by_xpath("//div[@class='WmcPopup-PopupContent']/div/button[2]").click()
    sleep(5)