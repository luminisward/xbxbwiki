from . import Page

class EnemyPage(Page):

    namespace = {
        'normal': '',
        'boss': '首领:',
        'unique': '冠名者:',
        'salvage': '打捞:'
    }

    core_crystal_drop_rate = {
        '1': '|普通核心水晶|5%|',
        '2': '|普通核心水晶|7.5%|',
        '3': '|普通核心水晶|12.5%|',
        '4': '|普通核心水晶|7.5%|\n|稀有核心水晶|1%|',
        '5': '|普通核心水晶|10%|\n|稀有核心水晶|3%|',
        '6': '|普通核心水晶|20%|\n|稀有核心水晶|6%|',
        '7': '|普通核心水晶|30%|\n|稀有核心水晶|9%|',
        '8': '|普通核心水晶|8%（初次100%）|\n|稀有核心水晶|3%|',
        '9': '|普通核心水晶|13%（初次100%）|\n|稀有核心水晶|8%（初次100%）|',
        '10': '|普通核心水晶|100%|',
        '11': '|普通核心水晶|100%|\n|稀有核心水晶|25%|',
        '12': '|普通核心水晶|100%|\n|稀有核心水晶|50%|',
        '13': '|普通核心水晶|100%|\n|稀有核心水晶|100%|',
        '14': '|普通核心水晶|20%（初次100%）|\n|稀有核心水晶|13%（初次100%）|\n|史诗核心水晶|3.9%|',
        '15': '|稀有核心水晶|50%（初次100%）|\n|史诗核心水晶|10%（初次100%）|',
        '16': '|普通核心水晶|100%|\n|稀有核心水晶|100%|\n|史诗核心水晶|5%|',
        'b1': '|普通核心水晶×3|100%|\n|稀有核心水晶|100%|',
        'b2': '|普通核心水晶×2|100%|\n|稀有核心水晶|100%|',
        'b3': '|稀有核心水晶|100%|',
        'b4': '|稀有核心水晶×2|100%|',
        'b5': '|稀有核心水晶×2|100%|\n|史诗核心水晶|100%|'
    }

    resist_level = {
        '0': '-',
        '1': '抵抗',
        '2': '无效'
    }

    item_level = {
        '1': '普通',
        '2': '稀有',
        '3': '史诗'
    }

    @property
    def path(self):
        if self.data['分类'] == 'normal':
            path = '敌人/' + self.data['出现地'] + '/' + self.data['简中']
        elif self.data['分类'] == 'unique':
            path = '敌人/冠名者/' + self.data['简中']
        elif self.data['分类'] == 'boss':
            path = '敌人/主线剧情/' + self.data['简中']
        elif self.data['分类'] == 'salvage':
            path = '敌人/打捞/' + self.data['简中']
        return path

    def build_wikitext(self):
        self.clear_wikitext()

        # H1
        title = self.data['简中']
        title = title.split('_')[0] # 同名敌人，去除名称后括号内的备注
        self.build_header(1, title)

        self.append_line('<WRAP group>')
        # 配图
        if self.data['分类'] == 'normal':
            self.append_line(
                '<WRAP right half>{{{{:敌人:{}:{}.jpg?640|}}}}</WRAP>'
                .format(self.data['出现地'], self.data['简中'])
            )
        elif self.data['分类'] == 'unique':
            self.append_line(
                '<WRAP right half>{{{{敌人:冠名者:{}.jpg?640|}}}}</WRAP>'
                .format(self.data['简中'])
            )
        elif self.data['分类'] == 'boss':
            self.append_line(
                '<WRAP right half>{{{{敌人:主线剧情:{}.jpg?640|}}}}</WRAP>'
                .format(self.data['简中'])
            )

        # 主信息
        text = ''
        try:
            min_level, max_level = self.data['等级'].split('-')
            text += '^等级|{} ～ {}|'.format(min_level, max_level)
        except ValueError:
            text += '^等级|{}|'.format(self.data['等级'])
        text += '\n'
        text += '^种族|{}|\n'.format(self.data['种族'])
        text += '^平时弱点|{}|\n'.format(self.data['平时弱点'])
        text += '^怒时弱点|{}|\n'.format(self.data['怒时弱点'])
        text += '^出现场所|{}|\n'.format(self.data['出现地'])
        if self.data['分类'] != 'boss':
            text += '^天气限定|{}|\n'.format(self.data['天气限定'])
            text += '^剧情进度|{}|\n'.format(self.data['剧情进度'])
        self.wrap_column_half(text)

        self.append_line('</WRAP>')

        # 战斗强度
        self.build_header(2, '战斗强度')

        # 能力值
        self.build_header(3, '能力值')
        if self.data['分类'] == 'normal':
            self.append_line('//等级范围内最低等级的能力值//')
        self.append_line('^  HP  ^  力量  ^  以太力  ^  灵巧  ^  敏捷  ^  运气  ^')
        self.append_line(
            '|  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |'
            .format(
                self.data['HP'], self.data['力量'], self.data['以太力'],
                self.data['灵巧'], self.data['敏捷'], self.data['运气']
            )
        )

        # 抗性
        self.build_header(3, '抗性')
        self.append_line('^  物理  ^  以太  ^  破防  ^  吹飞  ^  击退  ^')
        self.append_line(
            '|  {}%  |  {}%  |  {}  |  {}  |  {}  |'
            .format(
                self.data['物理抗性'], self.data['以太抗性'], self.resist_level[self.data['破防']],
                self.resist_level[self.data['吹飞']], self.resist_level[self.data['击退']]
            )
        )

        # 击杀奖励
        self.build_header(2, '击杀奖励')

        self.append_line('<WRAP group>')

        # 固定奖励基础值
        text = self.build_header(3, '固定奖励基础值', ret=True)
        text += '^  EXP  ^  金钱  ^  WP  ^  SP  ^\n'
        text += '|  {}  |  {}  |  {}  |  {}  |\n'.format(
            self.data['EXP'], self.data['Gil'], self.data['WP'], self.data['SP']
        )

        # 核心水晶掉率
        text += self.build_header(3, '核心水晶', ret=True)
        try:
            text += self.core_crystal_drop_rate[self.data['核心水晶']]
        except KeyError:
            text += '-'
        text += '\n'

        self.wrap_column_half(text)

        # 物品掉落
        text = self.build_header(3, '物品掉落', ret=True)
        if len(self.data['掉落']) > 3:
            item_list = self.split_item_drop(self.data['掉落'])
            text += '\n'.join(map(self.render_item_drop, item_list))
        else:
            text += '-'
        text += '\n'
        self.wrap_column_half(text)

        self.append_line('</WRAP>')

    def render_item_drop(self, item):
        item_name, item_drop_rates = item.split('(')
        item_drop_rates = item_drop_rates[:-1] # 去除末尾右括号

        result = []

        for item_drop_rate in item_drop_rates.split(' '):
            item_level = item_drop_rate.count('*') # 记录物品稀有度
            item_drop_rate = self.filter_asterisk(item_drop_rate) # 去除星号
            item_drop_rate = item_drop_rate.replace('F', '（初次100%）')
            result.append('|[[物品:' + item_name + self.item_level_symbol(item_level)
                          + ']]|' + item_drop_rate + '|')

        return '\n'.join(result)

    @staticmethod
    def split_item_drop(string):
        # 分割道具
        item_list = string.split(',')
        return item_list

    @staticmethod
    def filter_asterisk(string):
        return ''.join(list(filter(lambda x: x != '*', string)))

    @staticmethod
    def item_level_symbol(item_level):
        symbol = '◇'
        return symbol * int(item_level)
