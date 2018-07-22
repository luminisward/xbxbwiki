import sys
from lib.factory import Factory

class ParserFactory(Factory):

    def __init__(self, page_type):
        super().__init__(page_type)
        self.module = sys.modules[__name__]

    def create(self):
        class_name = self.page_type.capitalize() + 'Parser'
        try:
            parser = getattr(self.module, class_name)()
        except AttributeError:
            parser = getattr(self.module, 'Parser')()
        return parser

class Parser():

    def __init__(self):
        self.__data = []
        self.__result = []

    def process(self):
        self.result = self.source_data

    @property
    def source_data(self):
        return self.__data

    @source_data.setter
    def source_data(self, data):
        self.__data = data

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, data):
        self.__result = data

class ShopParser(Parser):
    def process(self):
        """ 重新组织数据结构，便于解析 """
        shops = dict()
        for row in self.source_data:
            shop_state = row.pop('地区')
            shop_name = row.pop('商店名')
            shop_location = row.pop('位置')
            shop_condition = row.pop('商店条件')
            path = shop_state + '/' + shop_name
            try:
                shops[path]
            except KeyError:
                # Data structure
                shops[path] = {
                    'path': path,
                    '商店名': shop_name,
                    '位置': shop_location,
                    '商店条件': shop_condition,
                    'goods': []
                }
            shops[path]['goods'].append(row)

        self.result = shops.values()

class EnemyParser(Parser):
    def process(self):
        for row in self.source_data:
            if row['简中'] and row['分类'] != 'quest':
                self.result.append(row)
