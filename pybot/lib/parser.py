from lib.factory import Factory


class ParserFactory(Factory):
    def create(self, page_type):
        return eval(page_type.capitalize() + 'Parser')() 

class Parser(object):

    def __init__(self):
        self.__data = [] 

    def process(self):
        pass

    @property
    def source_data(self):
        return self.__data

    @source_data.setter
    def source_data(self, data):
        self.__data = data

    @property
    def result(self):
        return iter(self.__data)

class ShopParser(Parser):
    def process(self):
        """ 重新组织数据结构，便于解析 """
        shops = dict()
        for row in self.source_data:
            shop_state = row.pop('地区')
            shop_name = row.pop('商店名')
            shop_location = row.pop('位置')
            path = shop_state + '/' + shop_name
            try:
                shops[path]
            except KeyError:
                # Data structure
                shops[path] = {
                    'path': path,
                    '商店名': shop_name,
                    '位置': shop_location,
                    'goods': []
                }
            shops[path]['goods'].append(row)
            
        self.source_data = list(shops.values())
