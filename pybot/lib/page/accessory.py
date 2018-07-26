from . import Page

class AccessoryPage(Page):
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
        text += '^ 分类 | 饰品 |\n'
        text += '^ 种类 | {} |\n'.format(self.data['种类'])
        text += '^ 效果 | {} |\n'.format(self.data['说明'])
        self.wrap_column_half(text)
        self.append_line('</WRAP>')

        # 获得方式
        self.build_header(2, '获得方式')

        self.append_line('<WRAP group>')

        # 敌人掉落
        text = self.build_header(3, '敌人掉落', ret=True)
        text += '{{backlinks>.#敌人}}\n'
        self.wrap_column_half(text)

        # 商店
        text = self.build_header(3, '商店', ret=True)
        text += '{{backlinks>.#商店}}\n'
        self.wrap_column_half(text)

        self.append_line('</WRAP>')

        # 挑战战斗
        text = self.build_header(3, '挑战战斗', ret=True)
        text += '{{backlinks>.#挑战战斗}}\n'
        self.wrap_column_half(text)
