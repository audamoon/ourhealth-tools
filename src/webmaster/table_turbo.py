from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from selenium.webdriver.common.by import By
from modules.WMManager import WMManager
from modules.WMElement import TurboMenu

gs = SheetManager("1_yFLyApmyz-ra-NS9kVnh2H5lka6pM-VnOzF6izsSdI")
driver = ChromeConfigurator.get_driver()
wm = WMManager(driver, gs)

#В переменной data_origin указываем источник таблицы 
data_origin = "https://webmaster.yandex.ru/site/https:neoplus-clinic.ru:443/turbo/settings/menu/"

#Разово собираем в файл, вызывая фукнции для сбора меню. top - верхнее меню, main - основное
#Не нужно вызывать фукнцию с меню, которое не обозначено
#В переменной project мы вписываем основной домен сайта (или что угодно, т.к переменная используется для наименования файла с полученными данными)
#Главное, чтобы переменная project соответствовала данным в столбце "Дополнительно", который должен быть заполнен той же строкой
#Это необходимо, чтобы программа корректно обеспечивала чтение

project = "neoplus-clinic.ru"
wm.getMenu(data_origin, 'top', project)
wm.getMenu(data_origin, 'main', project)

#После того, как мы собрали данные о меню, комментим вызовы функций getMenu

#доступные параметры для mods в модуле TurboMenu: top, main
#без main подключить top нельзя, таковы ограничения вебмастера

wm.start(TurboMenu, ["top", "main"])

#Если нам необходимо сохранить результат в таблицу, то вызываем фукнцию ниже и в переменную result_file_path подствляем пусть до логов
#Если не нужно, то комментим эту фукнцию
result_file_path = "logs\\result2023-11-22-16-25.txt"
wm.saveResult(result_file_path)