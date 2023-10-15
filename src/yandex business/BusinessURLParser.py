from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs") 


site_num = 0
#put emails here
CLINIC_EMAIL = ["svetlayalinia@yandex.ru"] 

row_ids = gs.reader.find_row_id_by_word("E:E", "НЕТ")
# row_ids = gs.reader.find_row_id_by_two_word("B:B","E:E",CLINIC_EMAIL[site_num].strip(),"НЕТ")
links_to_maps = gs.reader.read_range("D:D")

driver = ChromeConfigurator.get_driver()
wait = WebDriverWait(driver, 10)

for row_id in row_ids:
    link = links_to_maps[row_id-1][0]
    driver.get(link)
    #Save windows amount before
    start_windows = driver.window_handles
    driver.find_element(By.XPATH, "//span[text()='Исправить неточность']/parent::button").click()
    #wait until new windows open
    wait.until(EC.new_window_is_opened(start_windows))
    driver.switch_to.window(driver.window_handles[1])
    gs.writer.write_cell(f"E{row_id}",driver.current_url.replace('?utm_source=maps&utm_medium=org_card&utm_campaign=owner-button',""))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    sleep(1)
    