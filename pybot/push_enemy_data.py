import googleSheets
import dokuwiki
import enemy
import sys

def pushEnemyData(dataList, Dokuwiki):
    for dataDict in dataList:
        if dataDict['简中']:
            wikitext = enemy.EnemyPageBuilder(dataDict)

            # 页面路径
            if dataDict['分类'] == 'normal':
                path = '敌人:' + dataDict['出现地'] + ':' + dataDict['简中']
            elif dataDict['分类'] == 'unique':
                path = '敌人:冠名者:' + dataDict['简中']
            elif dataDict['分类'] == 'boss':
                path = '敌人:主线剧情:' + dataDict['简中']
            elif dataDict['分类'] == 'salvage':
                path = '敌人:打捞:' + dataDict['简中']
            else:
                continue

            wikitext.render(dataDict['分类'])
            Dokuwiki.pages.set(path, wikitext.getWikitext())
            print(dataDict['简中'])

if __name__ == '__main__':
    try:
        import config
    except ModuleNotFoundError:
        print('找不到config')
        sys.exit()
    
    try:
        wiki = dokuwiki.DokuWiki(config.siteurl ,config.username, config.password, True)
    except dokuwiki.DokuWikiError:
        print('Username or password is wrong ,can\'t access wiki')
        sys.exit()

    if config.DATA_SOURCE == 'CSV':
        # read CSV file
        dataTable = enemy.EnemyCSV(config.CSV_PATH)
        dictList = dataTable.getData()
    elif config.DATA_SOURCE == 'GoogleSheets':
        # Set sheet instance
        mysheet = googleSheets.GoogleSheets()
        mysheet.sheetId = config.SPREADSHEET_ID
        mysheet.range = config.RANGE_NAME
        # pull data
        mysheet.pullData()
        dictList = mysheet.dictList

    pushEnemyData(dictList, wiki)
