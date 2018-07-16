from .dokuwikitext import DokuwikiTextBuilder

class Shop(DokuwikiTextBuilder):

    def render(self):
        data = self.get_data()

        # H1
        title = data['商店名']
        self.appendWikitext(self.buildHeader(1, title))

        # 主信息
        self.appendLine('<WRAP group>')
        text = '地点：'
        text += '{}\n'.format(data['位置'])
        self.appendLine(self.wrapColumnHalf(text))
        self.appendLine('</WRAP>')

        # 商品列表
        self.appendWikitext(self.buildHeader(3, '商品'))

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
        self.appendLine(text)
