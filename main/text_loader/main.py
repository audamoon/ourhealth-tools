import os
from func.netcat_mgr import NetCatManager
from func.netcat_mgr import NetCatFunctions
from func.selenium_mgr import SeleniumManager
from time import sleep

choose = -1
sm = None
while choose != 0:
    print("Выберите нужное действие:")
    print("1 - собрать видимые активные разделы в файл;\n2 - открыть видимые разделы;\n3 - выбрать разделы;\n0 - выйти")
    choose = int(input("Ввод: "))
    if choose == 0:
        break
    if sm == None:
        sm = SeleniumManager()
        nm = NetCatManager("https://garmonia-stacionar.ru/netcat/admin/#object.list(162)",sm.driver)
        function_mgr = NetCatFunctions(nm,sm)
        function_mgr.choose_file_path(os.getcwd())
        nm.open_netcat()
        sleep(5)
    match choose:
        case 1:
            pass
        case 2:
            function_mgr.get_fields()
        case 3:
            function_mgr.choose_subs()
        case 4:
            function_mgr.get_URl()
        case 5:
            function_mgr.change_word_in_fields()
        case 6:
            function_mgr.change_all_names()
        case 7:
            pass
        case _:
            break