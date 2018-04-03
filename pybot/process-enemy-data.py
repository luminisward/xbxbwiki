import enemy

newTable = enemy.EnemyCSV('Enemy (4).csv')
newData = newTable.getData()

oldTable = enemy.EnemyCSV('enemy.csv')
olddata = oldTable.getData()

result = []
for row in olddata:
    for newValues in newData:
        if row['日文'] == newValues['日文'] and row['等级'] == newValues['等级']:
            for key, values in newValues.items():
                row[key] = values
        if not row['平时弱点']:
            row['平时弱点'] = '无'
        if not row['怒时弱点']:
            row['怒时弱点'] = '无'            
    result.append(row)

headers = ['id','日文','简中','page','出现地','分类','平时弱点','怒时弱点','种族','等级','力量','以太力','灵巧','敏捷','运气','HP','物理抗性','以太抗性','破防','吹飞','击退','EXP','Gil','WP','SP','核心水晶','平时属性','怒时属性']

resultTable = enemy.EnemyCSV('results.csv')
resultTable.saveData(headers, result)