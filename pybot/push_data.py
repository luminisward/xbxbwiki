'''Entry for push data'''

import sys
import argparse
from lib.google_sheets import GoogleSheets
from lib.push import Push

try:
    from config.mywiki import WIKI
    from config.sheets import SHEETS
except ModuleNotFoundError:
    sys.exit('找不到config')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Push data to wiki.')
    parser.add_argument('site', help='Site name included in config/mywiki.py')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='print which pages will be changed')

    args = parser.parse_args()

    site_config = WIKI[args.site]
    is_dry_run = args.dry_run

    for page_type, sheet_config in SHEETS.items():
        if sheet_config['SPREADSHEET_ID'] and sheet_config['RANGE_NAME']:

            sheet_data = GoogleSheets(
                spreadsheet_id=sheet_config['SPREADSHEET_ID'],
                range_name=sheet_config['RANGE_NAME']
                ).get_data().dict_list

            push = Push(page_type, sheet_data, site_config)
            push.execute(is_dry_run)
