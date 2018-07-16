import sys
from dokuwiki import DokuWiki, DokuWikiError
from lib.google_sheets import GoogleSheets
from lib.shop import Shop

try:
    from config.mywiki import WIKI
    import config.sheets as sheets
except ModuleNotFoundError:
    print('找不到config')
    sys.exit()

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

def push_shop_data(data_list, dokuwiki):
    for data_dict in data_list:
        print(data_dict['商店名'])
        path = '商店:' + data_dict['path']
        wikitext = Shop()
        wikitext.set_data(data_dict)
        wikitext.render()
        dokuwiki.pages.set(path, wikitext.getWikitext())

if __name__ == '__main__':
    siteurl = WIKI['development']['SITEURL']
    username = WIKI['development']['USERNAME']
    password = WIKI['development']['PASSWORD']

    try:
        wiki = DokuWiki(siteurl, username, password, True)
    except DokuWikiError:
        print('Username or password is wrong ,can\'t access wiki')
        sys.exit()

    # get sheet data
    data = GoogleSheets(
        spreadsheet_id=sheets.SHOP['SPREADSHEET_ID'],
        range_name=sheets.SHOP['RANGE_NAME']
        ).get_data().dict_list

    shop_list = parse_data(data)
    push_shop_data(shop_list, wiki)
