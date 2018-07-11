import json
import csv
from .dokuwikitext import DokuwikiTextBuilder

class Shop(DokuwikiTextBuilder):

    def __init__(self):
        super().__init__()

    def render(self):
        data = self.get_data()

        # H1
        title = data['name']
        self.appendWikitext(self.buildHeader(1, title))
