import enemy
import sys

def pushNormalEnemy(dataList, Dokuwiki):
    for dataDict in dataList:
        if dataDict['分类'] == 'normal':
            if dataDict['简中']:
                wikitext = enemy.EnemyPageBuilder(dataDict)
                wikitext.render('normal')
                path = '敌人:' + dataDict['出现地'] + ':' + dataDict['简中']
                Dokuwiki.pages.set(path, wikitext.getWikitext())
                print(dataDict['简中'])

def pushUniqueEnemy(dataList, Dokuwiki):
    for dataDict in dataList:
        if dataDict['分类'] == 'unique':
            if dataDict['简中']:
                wikitext = enemy.EnemyPageBuilder(dataDict)
                wikitext.render('unique')
                path = '敌人:冠名者:' + dataDict['简中']
                Dokuwiki.pages.set(path, wikitext.getWikitext())
                print(dataDict['简中'])

if __name__ == '__main__':
    from mywiki import wiki
    try:
        f = sys.argv[1]
        dataTable = enemy.EnemyCSV(f)
        dataList = dataTable.getData()

        pushNormalEnemy(dataList, wiki)
        pushUniqueEnemy(dataList, wiki)
    except IndexError as identifier:
        print('第一个参数请提供数据CSV的路径')
