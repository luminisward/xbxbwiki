from . import Page

class CollectionPage(Page):
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
        self.append_line('<WRAP column half>')
        self.append_line('^ 分类 | {} |'.format('收藏道具'))
        self.append_line('^ 种类 | {} |'.format(self.data['种类']))
        self.append_line('^ 稀有度 | {} |'.format(int(self.data['稀有度']) * '◇'))
        self.append_line('^ 获得地点 | {} |'.format(self.data['获得地点']))
        if self.data['种类'] == '敌人掉落':
            self.append_line('^ 相关任务 | [[任务/{}]] |'.format(self.data['相关任务']))
        self.append_line('</WRAP>')
        self.append_line('</WRAP>')


        if self.data['种类'] != '敌人掉落':
            # 获得方式
            self.build_header(2, '获得方式')
            # 采集
            self.build_header(3, '采集')
            self.append_line('{{backlinks>.#采集}}')
