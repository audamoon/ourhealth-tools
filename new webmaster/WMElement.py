from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from WMController import WMController

class WMElement(ABC):

    @abstractmethod
    def __init__(self, controller:WMController):
        self.controller = controller

    @abstractmethod
    def start(self, row_id, uri):
        self.controller.open_link(row_id, uri)
    
    def get_result(self):
        self.result = 1
        return self.result
    
class Test(WMElement):
    URI = "/serp-snippets/regions/"

    def __init__(self, controller):
        super().__init__(controller)

    def start(self, row_id):
        return super().start(row_id, self.URI)
    
    def get_result(self):
        return super().get_result()