import json
import csv
from .dokuwikitext import DokuwikiTextBuilder

class ItemPageBuilder(DokuwikiTextBuilder):

    def __init__(self):
        super().__init__()
        self.__item_data = {}

    def set_item_data(self, data):
        self.__item_data = data

    def render(self, item_type):
        item_types = ('增幅器', '收藏道具', '核心水晶', '收纳包道具', '情报道具',
                      '辅助核心', '饰品', '核心晶片', '贵重品', '气瓶', '宝藏')
        if item_type not in item_types:
            raise ValueError('Invalid itemType')

        if not self.__item_data:
            raise ValueError('item data is empty')

        item_data = self.__item_data

        # H1
        title = item_data['简中']
        self.append_wikitext(self.buildHeader(1, title))

        # 主信息
        self.append_line('<WRAP group>')
        text = ''
        text += '^分类|{}|\n'.format(item_data['分类'])
        try:
            text += '^效果说明|{}|\n'.format(item_data['说明'])
        except KeyError:
            text += '^效果说明|{}|\n'.format('')
        self.append_line(self.wrap_column_half(text))
        self.append_line('</WRAP>')

        # 获得方式
        self.append_line(self.buildHeader(2, '获得方式'))

        # 敌人掉落
        text = self.buildHeader(3, '敌人掉落')
        text += '{{backlinks>.#敌人}}'
        self.append_line('')
        self.append_line(self.wrap_column_half(text))

        # 挑战战斗
        text = self.buildHeader(3, '挑战战斗')
        text += '{{backlinks>.#挑战战斗}}'
        self.append_line('')
        self.append_line(self.wrap_column_half(text))
