import sys
import dokuwiki
from lib.google_sheets import GoogleSheets
from lib.shop import Shop

def parse_data(data_list):
    """ 重新组织数据结构，便于解析 """
    shops = dict()
    for row in data_list:
        shop_name = row.pop('商店')
        shop_location = row.pop('地点')
        try:
            shops[shop_name]
        except KeyError:
            shops[shop_name] = {
                'location': shop_location,
                'goods': []
            }
        shops[shop_name]['goods'].append(row)

    shop_list = []
    for k, v in shops.items():
        v['name'] = k
        shop_list.append(v)
    return shop_list

def push_shop_data(data_list, wiki):
    datalist = parse_data(data_list)
    for data_dict in data_list:
        path = '商店:' + data_dict['name']
        wikitext = Shop()
        wikitext.set_item_data(data_dict)
        wikitext.render(data_dict['分类'])
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

    # Set sheet instance
    item_sheet = GoogleSheets()
    item_sheet.sheet_id = SPREADSHEET_ID
    item_sheet.range = RANGE_NAME
    # pull data
    item_sheet.pull_data()
    dict_list = item_sheet.dict_list

    push_shop_data(dict_list, wiki)
