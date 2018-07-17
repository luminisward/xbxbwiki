from lib.factory import Factory

class PageFactory(Factory):
    def create(self, page_type):
        return eval(page_type.capitalize() + 'Page')()

class Page(object):

    def __init__(self):
        self.__wikitext = ''
        self.__data = {}

    def buildHeader(self, headerLevel, content):
        '''append header'''
        if 1 <= headerLevel <= 6 and isinstance(headerLevel, int):
            markup = ''
            for i in range(7 - headerLevel):
                markup += '='
            return markup + ' ' + content + ' ' + markup + '\n'
        else:
            raise ValueError('argument must be int between 1 and 6')

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    def append_line(self, content):
        '''append a line with any content'''
        self.append_wikitext(content + '\n')

    def append_wikitext(self, content):
        '''append string to wikitext'''
        self.__wikitext += content

    def get_wikitext(self):
        '''return wikitext'''
        return self.__wikitext

    def wrap_column_half(self, content):
        return '<WRAP column half>\n' + content + '</WRAP>'

    def append_clearfix(self):
        self.append_line('<WRAP clear/>')

    @property
    def path(self):
        return ''

    def build_wikitext(self):
        pass


class ShopPage(Page):

    @property
    def path(self):
        return '商店/' + self.data['path']

    def build_wikitext(self):
        data = self.data

        # H1
        title = data['商店名']
        self.append_wikitext(self.buildHeader(1, title))

        # 主信息
        self.append_line('<WRAP group>')
        text = '地点：'
        text += '{}\n'.format(data['位置'])
        self.append_line(self.wrap_column_half(text))
        self.append_line('</WRAP>')

        # 商品列表
        self.append_wikitext(self.buildHeader(3, '商品'))

        text = '^名称^价格^契约书^条件^\n'
        for row in data['goods']:
            if row['契约书（简）']:
                row['契约书（简）'] = '[[物品/' + row['契约书（简）'] + ']]'

            text += '| [[物品/{}]] | {} | {} | {} |\n'.format(
                row['商品名'],
                row['价格'],
                row['契约书（简）'],
                row['条件']
            )
        self.append_line(text)
