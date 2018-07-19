from . import Page

class ShopPage(Page):

    @property
    def path(self):
        return '商店/' + self.data['path']

    def build_wikitext(self):
        self.clear_wikitext()

        data = self.data

        # H1
        title = data['商店名']
        self.build_header(1, title)

        # 主信息
        self.append_line('<WRAP group>')
        text = '地点：'
        text += '{}\n'.format(data['位置'])
        self.wrap_column_half(text)
        self.append_line('</WRAP>')

        # 商品列表
        self.build_header(3, '商品')

        text = '^名称^价格^契约书^出现条件^\n'
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
