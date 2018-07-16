import sys
import dokuwiki
from lib.google_sheets import GoogleSheets
from lib.shop import Shop

def parse_data(data_list):
    """ 重新组织数据结构，便于解析 """
    shops = dict()
    for row in data_list:
        shop_state = row.pop('地区')
        shop_name = row.pop('商店名')
        shop_location = row.pop('位置')
        path = shop_state + '/' + shop_name
        try:
            shops[path]
        except KeyError:
            # Data structure
            shops[path] = {
                'path': path,
                '商店名': shop_name,
                '位置': shop_location,
                'goods': []
            }
        shops[path]['goods'].append(row)
    
    return list(shops.values())

def push_shop_data(data_list, wiki):
    for data_dict in data_list:
        print(data_dict['商店名'])
        path = '商店:' + data_dict['path']
        wikitext = Shop()
        wikitext.set_data(data_dict)
        wikitext.render()
        wiki.pages.set(path, wikitext.getWikitext())

if __name__ == '__main__':
    try:
        from config.mywiki import *
        from config.shop_sheet import *
    except ModuleNotFoundError:
        print('找不到config')
        sys.exit()

    try:
        wiki = dokuwiki.DokuWiki(siteurl, username, password, True)
    except dokuwiki.DokuWikiError:
        print('Username or password is wrong ,can\'t access wiki')
        sys.exit()

    # get sheet data
    sheet = GoogleSheets(SPREADSHEET_ID, RANGE_NAME)
    dict_list = sheet.get_data().dict_list

    shop_list = parse_data(dict_list)
    push_shop_data(shop_list, wiki)
