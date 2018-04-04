import enemy

def pushNormalEnemy(dataList, Dokuwiki):
    for dataDict in dataList:
        if dataDict['分类'] == 'normal':
            if dataDict['简中']:
                wikitext = enemy.EnemyPageBuilder(dataDict)
                wikitext.normalOutput()
                path = '敌人:' + dataDict['出现地'] + ':' + dataDict['简中']
                Dokuwiki.pages.set(path, wikitext.getWikitext())
                print(dataDict['简中'])

def pushUniqueEnemy(dataList, Dokuwiki):
    for dataDict in dataList:
        if dataDict['分类'] == 'unique':
            if dataDict['简中']:
                wikitext = enemy.EnemyPageBuilder(dataDict)
                wikitext.uniqueOutput()
                path = '敌人:冠名者:' + dataDict['简中']
                Dokuwiki.pages.set(path, wikitext.getWikitext())
                print(dataDict['简中'])

if __name__ == '__main__':
    from mywiki import wiki

    dataTable = enemy.EnemyCSV('enemy.csv')
    dataList = dataTable.getData()

    pushNormalEnemy(dataList, wiki)
    pushUniqueEnemy(dataList, wiki)