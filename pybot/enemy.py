import json
import csv
from dokuwikitext import DokuwikiTextBuilder

class EnemyCSV(object):

    def __init__(self, file):
        self.data = []
        self.file = file
        try:
            with open(file,'r') as f:
                f_csv = csv.DictReader(f)
                for row in f_csv:
                    self.data.append(row)
        except FileNotFoundError:
            open(file,'w').close()

    def readCsvFile(self, file):
        '''Read CSV file, return list[dict]'''
        self.data = []
        with open(file,'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.data.append(row)

    def readJsonFile(self, file):
        '''Read Json file, return list[dict]'''
        self.data = []
        with open(file, 'r') as f:
            self.data = json.load(f)

    def getData(self):
        return self.data

    def saveData(self, dataDict, headers=''):
        '''Save'''
        if headers == '':
            headers = ['id','日文','简中','page','出现地','分类','平时弱点','怒时弱点','种族','等级','力量','以太力','灵巧','敏捷','运气','HP','物理抗性','以太抗性','破防','吹飞','击退','EXP','Gil','WP','SP','核心水晶','平时属性','怒时属性']

        with open(self.file,'w') as f:
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
    coreCrystalDropRate = {
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
    resistLevel = {
        '0': '-',
        '1': '抵抗',
        '2': '无效'
    }

    def __init__(self, dataDict):
        self.wikitext = ''
        self.dataDict = dataDict
        title = dataDict['简中']
        title = title.split('_')[0] # 同名敌人，去除名称后括号内的备注
        self.appendWikitext(self.buildHeader(1, title))

    def render(self, enemyType):
        enemyTypes = ('normal', 'unique', 'boss', 'salvage')
        if enemyType not in enemyTypes:
            raise ValueError('Invalid EnemyType')

        dataDict = self.dataDict

        self.appendLine('<WRAP group>')
        # 配图
        if enemyType == 'normal':
            self.appendLine(
                    '<WRAP right half>{{{{:敌人:{}:{}.jpg?640|}}}}</WRAP>'
                .format(dataDict['出现地'], dataDict['简中'])
            )
        elif enemyType == 'unique':
            self.appendLine(
                    '<WRAP right half>{{{{敌人:冠名者:{}.jpg?640|}}}}</WRAP>'
                .format(dataDict['简中'])
            )
        elif enemyType == 'boss':
            self.appendLine(
                    '<WRAP right half>{{{{敌人:主线剧情:{}.jpg?640|}}}}</WRAP>'
                .format(dataDict['简中'])
            )
        self.appendLine('')

        # 主信息
        text = ''
        try:
            minLv, maxLv = dataDict['等级'].split('-')
            text += '^等级|{} ～ {}|'.format(minLv, maxLv)
        except ValueError:
            text += '^等级|{}|'.format(dataDict['等级'])
        text += '\n'
        text += '^种族|{}|\n'.format(dataDict['种族'])
        text += '^平时弱点|{}|\n'.format(dataDict['平时弱点'])
        text += '^怒时弱点|{}|\n'.format(dataDict['怒时弱点'])
        text += '^出现场所|{}|\n'.format(dataDict['出现地'])
        if enemyType != 'boss':
            text += '^天气限定|{}|\n'.format(dataDict['天气限定'])
        self.appendLine(self.wrapColumnHalf(text))

        self.appendLine('</WRAP>')

        # 战斗强度
        self.appendLine(self.buildHeader(2, '战斗强度'))
        
        # 能力值
        self.appendLine(self.buildHeader(3, '能力值'))
        if enemyType == 'normal':
            self.appendLine('//等级范围内最低等级的能力值//')
        self.appendLine('^  HP  ^  力量  ^  以太力  ^  灵巧  ^  敏捷  ^  运气  ^')
        self.appendLine('|  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |'.format(dataDict['HP'],dataDict['力量'],dataDict['以太力'],dataDict['灵巧'],dataDict['敏捷'],dataDict['运气']))
        self.appendLine('')

        # 抗性
        self.appendLine(self.buildHeader(3, '抗性'))
        self.appendLine('^  物理  ^  以太  ^  破防  ^  吹飞  ^  击退  ^')
        self.appendLine('|  {}%  |  {}%  |  {}  |  {}  |  {}  |'.format(dataDict['物理抗性'],dataDict['以太抗性'],self.resistLevel[dataDict['破防']],self.resistLevel[dataDict['吹飞']],self.resistLevel[dataDict['击退']]))
        self.appendLine('')

        # 击杀奖励
        self.appendLine(self.buildHeader(2, '击杀奖励'))
        
        self.appendLine('<WRAP group>')
        # 固定奖励基础值
        text = self.buildHeader(3, '固定奖励基础值')
        text += '\n'
        text += '^  EXP  ^  金钱  ^  WP  ^  SP  ^'
        text += '\n'
        text += '|  {}  |  {}  |  {}  |  {}  |'.format(dataDict['EXP'],dataDict['Gil'],dataDict['WP'],dataDict['SP'])
        text += '\n'
        self.appendLine(self.wrapColumnHalf(text))

        # 核心水晶掉率
        text = self.buildHeader(3, '核心水晶')
        text += '\n'
        if dataDict['核心水晶']:
            text += self.coreCrystalDropRate[dataDict['核心水晶']]
        else:
            text += '-'
        text += '\n'
        self.appendLine(self.wrapColumnHalf(text))
        
        self.appendLine('</WRAP>')

        # 道具掉率
        # self.appendLine(self.buildHeader(3, '道具掉落'))
