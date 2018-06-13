import unittest
from enemy import EnemyPageBuilder

class EnemyTestCase(unittest.TestCase):

    def setUp(self):
        self.page = EnemyPageBuilder()
        mock_data = {
            'id': '8',
            '日文': 'アーチャー・イグーナ',
            '简中': '蜥蜴人弓箭手',
            'page': '289',
            '出现地': '英维迪亚',
            '分类': 'normal',
            '天气限定': '-',
            '剧情进度': '-',
            '平时弱点': '无',
            '怒时弱点': '无',
            '种族': '人型',
            '等级': '15-20',
            '力量': '88',
            '以太力': '121',
            '灵巧': '91',
            '敏捷': '71',
            '运气': '49',
            'HP': '7022',
            '物理抗性': '10',
            '以太抗性': '0',
            '破防': '0',
            '吹飞': '0',
            '击退': '0',
            'EXP': '45',
            'Gil': '20',
            'WP': '11',
            'SP': '6',
            '核心水晶': '1',
            '平时属性': '',
            '怒时属性': '',
            '掉落': '人型猎人1(14%),移动治疗1(14%),武技仇恨值上升1(12%),丰饶项饰(**8.4% ***5.6%)'
        }
        self.page.set_enemy_data(mock_data)

    def test_split_item_drop(self):
        source = '以太防御提升2(9%),会心提升2(10.8%),必杀技Lv4强化2(12.6%),反噬防御2(13.5%),五芒晶片(12.6%),七色贝项圈(**7.2% ***4.8%)'
        target = ['以太防御提升2(9%)', '会心提升2(10.8%)', '必杀技Lv4强化2(12.6%)', '反噬防御2(13.5%)', '五芒晶片(12.6%)', '七色贝项圈(**7.2% ***4.8%)']
        
        self.assertEqual(target, self.page.split_item_drop(source))

    def test_render_item_drop(self):
        source = '以太防御提升2(9%)'
        target = '|以太防御提升2|9%|'
        self.assertEqual(target, self.page.render_item_drop(source))

        source = '拳法家护腕(**7.2% ***4.8%)'
        target = '|拳法家护腕|7.2%|\n|拳法家护腕|4.8%|'
        self.assertEqual(target, self.page.render_item_drop(source))

        
if __name__ == '__main__':
    unittest.main()
