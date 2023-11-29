## Установка
Для начала нам надо установить python 3.11 с официального сайта, в процессе установки обязательно добавляем его в PATH (там есть галочка)
Далее мы должны установить переменную среды **PYTHONPATH** и добавить в нее два источника:
```
{путь до папки ourhealth-tools}/libs/sheethelper
{путь до папки ourhealth-tools}/libs/gseleniumconf
```
Теперь заходим в консоль и пишем
```bash
cd {пусть до ourhealth-tools}
pip install -r requirements.txt
```
Ждем установки, далее мы должны установить Google Chrome 114 версии и отключить у него обновления
## Функционал
Импортируем основные классы.
```python
from sheethelper.manager import SheetManager
from gseleniumconf.chrome import ChromeConfigurator
from modules.WMManager import WMManager
```
Далее импортируем модули.
```python
from modules.WMElement import TurboMenu, Turbo, Counter, Region, Sitemap
```
Теперь мы инициализируем основные модули 
```python
gs = SheetManager("[id таблицы Google]")
driver = ChromeConfigurator.get_driver()
wm = WMManager(driver, gs)
```
Для запуска программы мы пишем 
```python
wm.start(RequireClass, ["action"])
```
Список классов и описание их действий:
1. Turbo
	1. add - добавляет турбо на поддомены
	2. delete - удаляет турбо с поддоменов
2. TurboMenu
	1. top - добавляет верхнее меню turbo
	2. main - добавляет основное меню turbo
3. Counter
	1. bypass - обходит и включает счетчики
4. Region
	1. add - добавляет регион
5. Sitemap
	1. reload - запускает обход сайтмапа
	2. delete - удаляет сайтмап
	3. add - добавляет сайтмап
### Turbo menu 
Это особый модуль, потому что перед его использованием необходимо это меню спарсить, для этого надо использовать 
```python
#Не забудь изменить your-domain
data_origin = "https://webmaster.yandex.ru/site/https:your-domain:443/turbo/settings/menu/"
#указать если надо разделить сохраненные меню
project = ""
#получить верхнее меню
wm.getMenu(data_origin, 'top', project)
#получить основное меню
wm.getMenu(data_origin, 'main', project)
```
После этого запускаем основную программу
```python
wm.start(TurboMenu, ["top", "main"])
```
И, если необходимо - сохраняем 
```python
result_file_path = "logs\\result2023-11-22-16-25.txt"
wm.saveResult(result_file_path)
```