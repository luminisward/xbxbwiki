class DokuwikiTextBuilder(object):

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

    def get_data(self):
        return self.__data

    def set_data(self, data):
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
