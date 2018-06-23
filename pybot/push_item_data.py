import sys
import dokuwiki
from lib.google_sheets import GoogleSheets
import lib.item as item

def push_item_data(data_list, wiki):
    for data_dict in data_list:
        if data_dict['简中']:
            print(data_dict['简中'])
            path = '物品:' + data_dict['简中']
            wikitext = item.ItemPageBuilder()
            wikitext.set_item_data(data_dict)
            if data_dict['分类'] != '收藏道具':
                wikitext.render(data_dict['分类'])
                wiki.pages.set(path, wikitext.getWikitext())

if __name__ == '__main__':
    try:
        from config.mywiki import *
        from config.item_sheet import *
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

    push_item_data(dict_list, wiki)
