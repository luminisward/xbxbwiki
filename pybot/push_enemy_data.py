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
        from mywiki import wiki
        f = sys.argv[1]
    except ModuleNotFoundError:
        print('找不到dokuwiki站点信息')
        sys.exit()
    except IndexError:
        print('第一个参数请提供数据CSV的路径')
        sys.exit()

    dataTable = enemy.EnemyCSV(f)
    dataList = dataTable.getData()
    pushEnemyData(dataList, wiki)
