from lib.factory import Factory

class PageFactory(Factory):
    def create(self, page_type):
        return eval(page_type.capitalize() + 'Page')()


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

        if ret == False:
            self.append_line(markup + ' ' + content + ' ' + markup)
        else:
            return markup + ' ' + content + ' ' + markup + '\n'



    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
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
        self.append_line('<WRAP column half>\n' + content + '</WRAP>')

    def append_clearfix(self):
        self.append_line('<WRAP clear/>')


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
        self.append_line(text)

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
        data = self.data

        # H1
        title = data['简中']
        title = title.split('_')[0] # 同名敌人，去除名称后括号内的备注
        self.build_header(1, title)

        self.append_line('<WRAP group>')
        # 配图
        if data['分类'] == 'normal':
            self.append_line(
                '<WRAP right half>{{{{:敌人:{}:{}.jpg?640|}}}}</WRAP>'
                .format(data['出现地'], data['简中'])
            )
        elif data['分类'] == 'unique':
            self.append_line(
                '<WRAP right half>{{{{敌人:冠名者:{}.jpg?640|}}}}</WRAP>'
                .format(data['简中'])
            )
        elif data['分类'] == 'boss':
            self.append_line(
                '<WRAP right half>{{{{敌人:主线剧情:{}.jpg?640|}}}}</WRAP>'
                .format(data['简中'])
            )
        self.append_line('')

        # 主信息
        text = ''
        try:
            min_level, max_level = data['等级'].split('-')
            text += '^等级|{} ～ {}|'.format(min_level, max_level)
        except ValueError:
            text += '^等级|{}|'.format(data['等级'])
        text += '\n'
        text += '^种族|{}|\n'.format(data['种族'])
        text += '^平时弱点|{}|\n'.format(data['平时弱点'])
        text += '^怒时弱点|{}|\n'.format(data['怒时弱点'])
        text += '^出现场所|{}|\n'.format(data['出现地'])
        if data['分类'] != 'boss':
            text += '^天气限定|{}|\n'.format(data['天气限定'])
            text += '^剧情进度|{}|\n'.format(data['剧情进度'])
        self.wrap_column_half(text)

        self.append_line('</WRAP>')

        # 战斗强度
        self.build_header(2, '战斗强度')

        # 能力值
        self.build_header(3, '能力值')
        if data['分类'] == 'normal':
            self.append_line('//等级范围内最低等级的能力值//')
        self.append_line('^  HP  ^  力量  ^  以太力  ^  灵巧  ^  敏捷  ^  运气  ^')
        self.append_line(
            '|  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |'
            .format(
                data['HP'], data['力量'], data['以太力'],
                data['灵巧'], data['敏捷'], data['运气']
            )
        )
        self.append_line('')

        # 抗性
        self.build_header(3, '抗性')
        self.append_line('^  物理  ^  以太  ^  破防  ^  吹飞  ^  击退  ^')
        self.append_line(
            '|  {}%  |  {}%  |  {}  |  {}  |  {}  |'
            .format(
                data['物理抗性'], data['以太抗性'], self.resist_level[data['破防']],
                self.resist_level[data['吹飞']], self.resist_level[data['击退']]
            )
        )
        self.append_line('')

        # 击杀奖励
        self.build_header(2, '击杀奖励')

        self.append_line('<WRAP group>')

        # 固定奖励基础值
        text = self.build_header(3, '固定奖励基础值', ret=True)
        text += '\n'
        text += '^  EXP  ^  金钱  ^  WP  ^  SP  ^'
        text += '\n'
        text += '|  {}  |  {}  |  {}  |  {}  |'.format(
            data['EXP'], data['Gil'], data['WP'], data['SP']
        )
        text += '\n'

        # 核心水晶掉率
        text += self.build_header(3, '核心水晶', ret=True)
        text += '\n'
        try:
            text += self.core_crystal_drop_rate[data['核心水晶']]
        except KeyError:
            text += '-'
        text += '\n'

        self.wrap_column_half(text)

        # 物品掉落
        text = self.build_header(3, '物品掉落', ret=True)
        text += '\n'
        if len(data['掉落']) > 3:
            item_list = self.split_item_drop(data['掉落'])
            text += '\n'.join(map(self.render_item_drop, item_list))
        else:
            text += '-'
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
