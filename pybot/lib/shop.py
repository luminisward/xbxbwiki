import json
import csv
from .dokuwikitext import DokuwikiTextBuilder

class Shop(DokuwikiTextBuilder):

    def __init__(self):
        super().__init__()
        self.__data = {}

    def set_item_data(self, data):
        self.__data = data

    def render(self, item_type):
        pass
