from . import Page

class Pouch_itemPage(Page):
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
        text += '^ 分类 | {} |\n'.format('收纳包道具')
        text += '^ 种类 | {} |\n'.format(self.data['种类'])
        text += '^ 出售价格 | {} G |\n'.format(self.data['卖价'])
        text += '^ 稀有度 | {} |\n'.format(int(self.data['稀有度']) * '◇')
        if self.data['相关任务'] != '':
            text += '^ 相关任务 | [[任务/普通任务/{}]] |\n'.format(self.data['相关任务'])
        self.wrap_column_half(text)

        text = ''
        text += '^ 效果时间 | {} 分钟 |\n'.format(self.data['效果时间'])
        text += '^ 道具效果 | {} |\n'.format(self.data['效果1'])
        if self.data['效果2'] != '':
            text += '^ ::: | {} |\n'.format(self.data['效果2'])
        if self.data['效果3'] != '':
            text += '^ ::: | {} |\n'.format(self.data['效果3'])
        text += '^ 异刃信赖度增加 | {} |\n'.format(self.data['信赖度'])
        self.wrap_column_half(text)

        self.append_line('</WRAP>')

        # 获得方式
        self.build_header(2, '获得方式')

        if self.data['制作']: # 制作
            self.build_header(3, '制作')
            self.append_line('  * [[商店/{}]]'.format(self.data['制作']))
        else: # 商店
            self.build_header(3, '商店')
            self.append_line('{{backlinks>.#商店}}')
