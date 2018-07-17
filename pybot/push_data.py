from config.sheets import SHEETS

def push(table_name):
    pass

push_list = []
for key, value in SHEETS.items():
    if value['SPREADSHEET_ID'] and value['RANGE_NAME']:
        push_list.append(key)

print(push_list)

map(push, push_list)
