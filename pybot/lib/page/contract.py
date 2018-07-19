from . import Page

class ContractPage(Page):
    @property
    def path(self):
        return '物品/' + self.data['简中']

    def build_wikitext(self):
        self.clear_wikitext()

        # H1
        title = self.data['简中']
        self.build_header(1, title)

        # 主信息
        self.append_line('<WRAP group>')

        text = ''
        text += '^分类|{}|\n'.format('贵重品')
        text += '^种类|{}|\n'.format('契约书')
        self.wrap_column_half(text)

        text = ''
        text += '对应商店\n'
        text += '{{backlinks>.#商店}}'
        self.wrap_column_half(text)

        self.append_line('</WRAP>')

        # 获得方式
        self.build_header(2, '获得方式')

        # 佣兵团任务
        self.build_header(3, '佣兵团任务')
        self.append_line('{{backlinks>.#佣兵团}}')
