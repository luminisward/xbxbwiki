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

    try:
        # Select site config and test connection
        site_config = WIKI[sys.argv[1]]
        wiki = DokuWiki(
            site_config['SITEURL'],
            site_config['USERNAME'],
            site_config['PASSWORD'],
            cookieAuth=True
        )

    except IndexError:
        # 命令没带参数
        print('Tell me which website you want to push data.')

    except KeyError:
        # 未匹配到mywiki.py配置中的站点
        print('Invalid site.')

    except DokuWikiError:
        print('Username or password is wrong ,can\'t access wiki.')

    else:
        # get sheet data
        data = GoogleSheets(
            spreadsheet_id=sheets.SHOP['SPREADSHEET_ID'],
            range_name=sheets.SHOP['RANGE_NAME']
            ).get_data().dict_list

        shop_list = parse_data(data)
        push_shop_data(shop_list, wiki)
