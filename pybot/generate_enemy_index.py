import enemy

dataTable = enemy.EnemyCSV('enemy.csv')
dataList = dataTable.getData()
print(len(dataList))

dataList = sorted(dataList, key=lambda x: x['出现地'], reverse=True)

for dataDict in dataList:
    if dataDict['分类'] == 'normal':
        if dataDict['简中']:
            path = '敌人:' + dataDict['出现地'] + ':' + dataDict['简中']
            with open('index.txt','a') as f:
                f.write('|[[{}]]|{}|\n'.format(path,dataDict['出现地']))
            print(dataDict['简中'])