from gseleniumconf.chrome import ChromeConfigurator
from sheethelper.manager import SheetManager

gs = SheetManager()
gs.start_service("1ICruRu0RJi7dmyf7ugAo7poE6SvFuoiVns3Tv29aeQs")
table_data = gs.reader.read_range("H323:M323")[0]
numbers = table_data[:2]
socials = table_data[2:]
print(numbers)
print(socials)