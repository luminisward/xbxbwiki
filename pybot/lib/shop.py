import json
import csv
from .dokuwikitext import DokuwikiTextBuilder

class Shop(DokuwikiTextBuilder):

    def __init__(self):
        super().__init__()

    def render(self):
        data = self.get_data()

        # H1
        title = data['商店名']
        self.appendWikitext(self.buildHeader(1, title))

        # 主信息
        self.appendLine('<WRAP group>')
        text = ''
        text += '{}\n'.format(data['位置'])
        self.appendLine(self.wrapColumnHalf(text))
        self.appendLine('</WRAP>')

        # 商品列表
        self.appendWikitext(self.buildHeader(3, '商品'))

        text = '^名称^稀有度^价格^条件^\n'
        for row in data['goods']:
            try:
                text += '|[[物品/{}]]|{}|{}|{}|\n'.format(*row.values())
            except IndexError:
                text += '|[[物品/{}]]|{}|{}| |\n'.format(*row.values())
        self.appendLine(text)
