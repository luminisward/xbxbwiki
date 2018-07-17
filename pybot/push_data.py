import sys
from dokuwiki import DokuWiki, DokuWikiError
from lib.page import PageFactory
from lib.parser import ParserFactory
from lib.google_sheets import GoogleSheets

try:
    from config.mywiki import WIKI
    from config.sheets import SHEETS
except ModuleNotFoundError:
    print('找不到config')
    sys.exit()


def pull_sheet_data(page_type):
    ''' Get sheet data from Internet '''
    sheet_data = GoogleSheets(
        spreadsheet_id=SHEETS[page_type]['SPREADSHEET_ID'],
        range_name=SHEETS[page_type]['RANGE_NAME']
        ).get_data().dict_list
    return sheet_data

def push(page_type, data):
    '''Push data to wiki'''
    # Process original data
    parser = ParserFactory().create(page_type)
    parser.source_data = data
    parser.process()
    processed_data = parser.result

    # Iterate data for
    for data_row in processed_data:
        page = PageFactory().create(page_type)
        page.data = data_row
        page.build_wikitext()
        wiki.pages.set(page.path, page.get_wikitext())
        print(page.path)


if __name__ == '__main__':

    try:
        # Select site config and test connection
        SITE_CONFIG = WIKI[sys.argv[1]]

        wiki = DokuWiki(
            SITE_CONFIG['SITEURL'],
            SITE_CONFIG['USERNAME'],
            SITE_CONFIG['PASSWORD'],
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
        for page_type, sheet_config in SHEETS.items():
            if sheet_config['SPREADSHEET_ID'] and sheet_config['RANGE_NAME']:
                data = pull_sheet_data(page_type)
                push(page_type, data)
