import json
import csv
from dokuwikitext import DokuwikiTextBuilder

class EnemyCSV(object):

    def __init__(self, file):
        self.data = []
        self.file = file
        try:
            with open(file, 'r') as f:
                f_csv = csv.DictReader(f)
                for row in f_csv:
                    self.data.append(row)
        except FileNotFoundError:
            open(file, 'w').close()

    def read_csv_file(self, file):
        '''Read CSV file, return list[dict]'''
        self.data = []
        with open(file, 'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.data.append(row)

    def read_json_file(self, file):
        '''Read Json file, return list[dict]'''
        self.data = []
        with open(file, 'r') as f:
            self.data = json.load(f)

    def get_data(self):
        return self.data

    def save_data(self, dataDict, headers=''):
        '''Save'''
        if headers == '':
            headers = [
                'id', '日文', '简中', 'page', '出现地', '分类', '平时弱点', '怒时弱点',
                '种族', '等级', '力量', '以太力', '灵巧', '敏捷', '运气', 'HP', '物理抗性',
                '以太抗性', '破防', '吹飞', '击退', 'EXP', 'Gil', 'WP', 'SP', '核心水晶',
                '平时属性', '怒时属性'
            ]

        with open(self.file, 'w') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(dataDict)

class EnemyPageBuilder(DokuwikiTextBuilder):

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

    def __init__(self, data):
        self.enemy_data = data
        title = data['简中']
        title = title.split('_')[0] # 同名敌人，去除名称后括号内的备注
        super().__init__(title)

    def render(self, enemy_type):
        enemy_types = ('normal', 'unique', 'boss', 'salvage')
        if enemy_type not in enemy_types:
            raise ValueError('Invalid EnemyType')

        enemy_data = self.enemy_data

        self.appendLine('<WRAP group>')
        # 配图
        if enemy_type == 'normal':
            self.appendLine(
                '<WRAP right half>{{{{:敌人:{}:{}.jpg?640|}}}}</WRAP>'
                .format(enemy_data['出现地'], enemy_data['简中'])
            )
        elif enemy_type == 'unique':
            self.appendLine(
                '<WRAP right half>{{{{敌人:冠名者:{}.jpg?640|}}}}</WRAP>'
                .format(enemy_data['简中'])
            )
        elif enemy_type == 'boss':
            self.appendLine(
                '<WRAP right half>{{{{敌人:主线剧情:{}.jpg?640|}}}}</WRAP>'
                .format(enemy_data['简中'])
            )
        self.appendLine('')

        # 主信息
        text = ''
        try:
            min_level, max_level = enemy_data['等级'].split('-')
            text += '^等级|{} ～ {}|'.format(min_level, max_level)
        except ValueError:
            text += '^等级|{}|'.format(enemy_data['等级'])
        text += '\n'
        text += '^种族|{}|\n'.format(enemy_data['种族'])
        text += '^平时弱点|{}|\n'.format(enemy_data['平时弱点'])
        text += '^怒时弱点|{}|\n'.format(enemy_data['怒时弱点'])
        text += '^出现场所|{}|\n'.format(enemy_data['出现地'])
        if enemy_type != 'boss':
            text += '^天气限定|{}|\n'.format(enemy_data['天气限定'])
            text += '^剧情进度|{}|\n'.format(enemy_data['剧情进度'])
        self.appendLine(self.wrapColumnHalf(text))

        self.appendLine('</WRAP>')

        # 战斗强度
        self.appendLine(self.buildHeader(2, '战斗强度'))

        # 能力值
        self.appendLine(self.buildHeader(3, '能力值'))
        if enemy_type == 'normal':
            self.appendLine('//等级范围内最低等级的能力值//')
        self.appendLine('^  HP  ^  力量  ^  以太力  ^  灵巧  ^  敏捷  ^  运气  ^')
        self.appendLine(
            '|  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |'
            .format(
                enemy_data['HP'], enemy_data['力量'], enemy_data['以太力'],
                enemy_data['灵巧'], enemy_data['敏捷'], enemy_data['运气']
            )
        )
        self.appendLine('')

        # 抗性
        self.appendLine(self.buildHeader(3, '抗性'))
        self.appendLine('^  物理  ^  以太  ^  破防  ^  吹飞  ^  击退  ^')
        self.appendLine(
            '|  {}%  |  {}%  |  {}  |  {}  |  {}  |'
            .format(
                enemy_data['物理抗性'], enemy_data['以太抗性'], self.resist_level[enemy_data['破防']],
                self.resist_level[enemy_data['吹飞']], self.resist_level[enemy_data['击退']]
            )
        )
        self.appendLine('')

        # 击杀奖励
        self.appendLine(self.buildHeader(2, '击杀奖励'))

        self.appendLine('<WRAP group>')
        # 固定奖励基础值
        text = self.buildHeader(3, '固定奖励基础值')
        text += '\n'
        text += '^  EXP  ^  金钱  ^  WP  ^  SP  ^'
        text += '\n'
        text += '|  {}  |  {}  |  {}  |  {}  |'.format(
            enemy_data['EXP'], enemy_data['Gil'], enemy_data['WP'], enemy_data['SP']
        )
        text += '\n'
        self.appendLine(self.wrapColumnHalf(text))

        # 核心水晶掉率
        text = self.buildHeader(3, '核心水晶')
        text += '\n'
        try:
            text += self.core_crystal_drop_rate[enemy_data['核心水晶']]
        except KeyError:
            text += '-'
        text += '\n'
        self.appendLine(self.wrapColumnHalf(text))

        self.appendLine('</WRAP>')

        # 道具掉率
        # self.appendLine(self.buildHeader(3, '道具掉落'))

    def item_drop(self):
        pass
