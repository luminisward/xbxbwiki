class DokuwikiTextBuilder(object):

    def __init__(self, title):
        self.wikitext = ''
        self.appendWikitext(self.buildHeader(1, title))

    def buildHeader(self, headerLevel, content):
        '''append header'''
        if 1 <= headerLevel <= 6 and isinstance(headerLevel, int):
            markup = ''
            for i in range(7 - headerLevel):
                markup += '='
            return markup + ' ' + content + ' ' + markup + '\n'
        else:
            raise ValueError('argument must be int between 1 and 6')

    def appendLine(self, content):
        '''append a line with any content'''
        self.appendWikitext(content + '\n')

    def appendWikitext(self, content):
        '''append string to wikitext'''
        self.wikitext += content

    def getWikitext(self):
        '''return wikitext'''
        return self.wikitext

    def wrapColumnHalf(self, content):
        return '<WRAP column half>\n' + content + '</WRAP>'

    def appendClearfix(self):
        self.appendLine('<WRAP clear/>')
