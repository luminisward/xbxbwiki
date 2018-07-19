'''Entry for push data'''

import sys
from lib.google_sheets import GoogleSheets
from lib.push import Push

try:
    from config.mywiki import WIKI
    from config.sheets import SHEETS
except ModuleNotFoundError:
    print('找不到config')
    sys.exit()

if __name__ == '__main__':

    try:
        # Select site config and test connection
        SITE_CONFIG = WIKI[sys.argv[1]]

    except IndexError:
        # 命令没带参数
        sys.exit('未指定站点名参数\ne.g. "python push_data.py development"')

    except KeyError:
        sys.exit('mywiki.py中找不到' + sys.argv[1] + '站点的配置')

    else:
        for page_type, sheet_config in SHEETS.items():
            if sheet_config['SPREADSHEET_ID'] and sheet_config['RANGE_NAME']:

                sheet_data = GoogleSheets(
                    spreadsheet_id=sheet_config['SPREADSHEET_ID'],
                    range_name=sheet_config['RANGE_NAME']
                    ).get_data().dict_list

                push = Push(page_type, sheet_data, SITE_CONFIG)
                push.execute()
