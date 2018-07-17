from config.sheets import SHEETS
from lib.page import Page

def push(table_name):
    data = GoogleSheets(
        spreadsheet_id=SHEETS[table_name]['SPREADSHEET_ID'],
        range_name=SHEETS[table_name]['RANGE_NAME']
        ).get_data().dict_list
    p = Page().get_page(table_name)
    p.set_data(data_dict)
    p.render()
    dokuwiki.pages.set(path, p.getWikitext())

push_list = []
for key, value in SHEETS.items():
    if value['SPREADSHEET_ID'] and value['RANGE_NAME']:
        push_list.append(key)

print(push_list)

map(push, push_list)
