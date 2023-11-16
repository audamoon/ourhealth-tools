from source.sheet.manager import GoogleSheetReader
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class WebElement(ABC):
    @abstractmethod
    def set_columns(self, *args):
        pass 

BeautifulSoup


class WebOpener(WebElement):
    


    # def open_url(self, sheet_reader: GoogleSheetReader, subfolder: str):
    #     sheet_reader.

class WebmasterManager:
    def set_columns(self, city_name: str = "A", domain_link: str = "B", result: str = "C",
                    additional_info: str = "D",link_to_webmaster: str = "E"):
        self.columns = {}
        self.columns["city_name"] = city_name
        self.columns["domain_link"] = domain_link
        self.columns["result"] = result
        self.columns["additional_info"] = additional_info
        self.columns["link_to_webmaster"] = link_to_webmaster





master = WebmasterManager()
master.set_columns()
