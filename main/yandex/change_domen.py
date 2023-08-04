from func.selenium_mgr import SeleniumManager
from selenium.webdriver.common.by import By
from func.google_sheet_mgr import SheetManager
from time import sleep
gs = SheetManager("1WsAf_t2PuLD4qowmv5zYyp7YMNpyuSsN0Ir35u5aWQk")
sm = SeleniumManager()

# a = gs.get_values("C")
# row_array = []
# for j in range(len(a)):
#     for el in a[j]:
#         if el == "Что-то не так":
#             row_array.append(j+1)
# for row_id in row_array:
for i in range (379,420):
    old_url = gs.read_cell("A",True,i)
    new_url = gs.read_cell("B",True,i)
    chopped_old_url = old_url.split("//")
    chopped_new_url = new_url.split("//")
    link = f"https://webmaster.yandex.ru/site/{chopped_old_url[0]}{chopped_old_url[1]}:443/indexing/mirrors/"
    sm.driver.get(link)
    sleep(2)
    try: 
        sm.driver.find_element(By.XPATH,"//span[contains(text(),'Заявка от')]")
        gs.write_cell("C","Добавлен",True,i)
    except:
        try:
            sm.driver.find_element(By.XPATH,"//span[contains(text(),'В ближайшее время')]")
            gs.write_cell("C","Добавлен",True,i)
        except:
            gs.write_cell("C","Что-то не так",True,i)


    # добавление домена
    # sm.wait_until_presence("(//input[@class='Textinput-Control'])[4]")
    # sleep(2)
    # try:
    #     sm.driver.find_element(By.XPATH,"//span[contains(text(),'Заявка от')]")
    #     gs.write_cell("C","Уже был",True,i)
    # except:
    #     input = sm.el_by_xpath("(//input[@class='Textinput-Control'])[4]")
    #     input.click()
    #     input.clear()
    #     input.send_keys(chopped_new_url[1])
    #     sm.wait_until_presence(f"(//span[@class='Link SitesSuggest-Link'][contains(text(),'{chopped_new_url[1]}')])[1]")
    #     sm.el_by_xpath(f"(//span[@class='Link SitesSuggest-Link'][contains(text(),'{chopped_new_url[1]}')])[1]").click()
    #     sm.el_by_xpath("//button[@class='Button2 Button2_view_action Button2_size_m']").click()
    #     try:
    #         sm.wait_until_presence("//span[contains(text(),'Заявка от')]",5)
    #         gs.write_cell("C","Добавлен",True,i)
    #     except:
    #         gs.write_cell("C","Что-то не так",True,i)
    

