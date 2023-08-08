from func.selenium_mgr import SeleniumManager
sm = SeleniumManager()
sm.driver.get("https://webmaster.yandex.ru/site/https:achinsk.delta-clinic.ru:443/indexing/sitemap/")
btn = sm.el_by_xpath("//button[contains(@class,'button_size_xs')]/parent::div")
btn.click()
sm.wait_until_presence("//div[@class='tooltip__content'][contains(text(),'Файл был отправлен на переобход')]")