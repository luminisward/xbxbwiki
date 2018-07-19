import sys
from lib.factory import Factory

class PageFactory(Factory):

    def __init__(self, page_type):
        super().__init__(page_type)
        self.module_name = '.'.join([__name__, page_type.lower()])
        __import__(self.module_name)

    def create(self):
        module = sys.modules[self.module_name]
        class_name = self.page_type.capitalize() + 'Page'
        return getattr(module, class_name)()

class Page():

    def __init__(self):
        self.__wikitext = ''
        self.__data = {}

    @property
    def path(self):
        return ''

    def clear_wikitext(self):
        self.__wikitext = ''

    def build_wikitext(self):
        pass

    def build_header(self, header_level, content, ret=False):
        '''append header'''
        if 1 <= header_level <= 6 and isinstance(header_level, int):
            markup = '=' * (7 - header_level)
        else:
            raise ValueError('argument must be int between 1 and 6')

        if ret is False:
            self.append_line(markup + ' ' + content + ' ' + markup)
        return markup + ' ' + content + ' ' + markup + '\n'

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    def append_line(self, content=''):
        '''append a line with any content'''
        self.append_wikitext(content + '\n')

    def append_wikitext(self, content=''):
        '''append string to wikitext'''
        self.__wikitext += content

    def get_wikitext(self):
        '''return wikitext'''
        return self.__wikitext

    def wrap_column_half(self, content=''):
        self.append_line('<WRAP column half>\n' + content + '</WRAP>')

    def append_clearfix(self):
        self.append_line('<WRAP clear/>')
