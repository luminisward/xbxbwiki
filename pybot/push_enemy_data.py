import sys
import dokuwiki
from lib.google_sheets import GoogleSheets
import lib.enemy as enemy

def push_enemy_data(data_list, wiki):
    for data_dict in data_list:
        if data_dict['简中']:

            # 页面路径
            if data_dict['分类'] == 'normal':
                path = '敌人:' + data_dict['出现地'] + ':' + data_dict['简中']
            elif data_dict['分类'] == 'unique':
                path = '敌人:冠名者:' + data_dict['简中']
            elif data_dict['分类'] == 'boss':
                path = '敌人:主线剧情:' + data_dict['简中']
            elif data_dict['分类'] == 'salvage':
                path = '敌人:打捞:' + data_dict['简中']
            else:
                continue

            wikitext = enemy.EnemyPageBuilder()
            wikitext.set_enemy_data(data_dict)
            wikitext.render(data_dict['分类'])
            wiki.pages.set(path, wikitext.getWikitext())
            print(data_dict['简中'])

if __name__ == '__main__':
    try:
        from config.mywiki import *
        from config.enemy_sheet import *
    except ModuleNotFoundError:
        print('找不到config')
        sys.exit()

    try:
        wiki = dokuwiki.DokuWiki(siteurl, username, password, True)
    except dokuwiki.DokuWikiError:
        print('Username or password is wrong ,can\'t access wiki')
        sys.exit()

    if DATA_SOURCE == 'CSV':
        # read CSV file
        data_table = enemy.EnemyCSV(CSV_PATH)
        dict_list = data_table.get_data()
    elif DATA_SOURCE == 'GoogleSheets':
        # Set sheet instance
        enemy_sheet = GoogleSheets()
        enemy_sheet.sheet_id = SPREADSHEET_ID
        enemy_sheet.range = RANGE_NAME
        # pull data
        enemy_sheet.pull_data()
        dict_list = enemy_sheet.dict_list

    push_enemy_data(dict_list, wiki)
