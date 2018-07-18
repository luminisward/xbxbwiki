## 环境

进入python环境

    ./enter-python-environment.sh 

pip安装依赖，保存路径已改成`.local`

    pip install -r requirements.txt

## dokuwiki API

文档：

http://python-dokuwiki.readthedocs.io/en/latest/

### wiki配置

* 参考修改`config/mywiki.example.py`文件，并重命名为`config/mywiki.py`
* `WIKI['development']`中的`development`为站点名，方便多站点配置，具体名称可自行更改
* push_data脚本以站点名为唯一的命令行参数，以区分操作目标

## Google Sheets

新增了从Google Sheets获取数据的功能

### Quickstart

原文： https://developers.google.com/sheets/api/quickstart/python

1. 先去[这里](https://console.developers.google.com/flows/enableapi?apiid=sheets.googleapis.com)创建项目，获取客户端ID和密钥 
2. 下载到包含客户端ID和密钥的`credentials.json`，置于当前目录下
3. 执行`python get_token.py`获取token，如果使用了虚拟环境（比如上面推荐的docker）往下看
4. 执行`python get_token.py --noauth_local_webserver`，手动打开浏览器授权，网页上会提供一串校验码，粘贴进终端后完成验证
5. 目录下生成`token.json`文件，说明验证完成，可以使用Google API了

### Sheet数据源配置

* 参考修改`config/sheets.example.py`文件，并重命名为`config/sheets.py`
* **SPREADSHEET_ID** 和 **RANGE_NAME** 都为空的项目将会被忽略，非空项目将会被依次拉取并推送到目标站点上
* **ACCESSORY** 等一级属性对应模块`lib.page`和`lib.parser`中的类，不可改名

## 推送脚本使用说明

脚本入口：`python push_data.py development`

唯一的参数：对应`config/mywiki.py`中的站点名

### 操作流程

1. 第一次使用需要配置API密钥，见[Quickstart](#Quickstart)
2. 修改配置`config/mywiki.py`中的多站点信息
3. 修改配置`config/sheets.py`中的数据表信息
4. 执行`python push_data.py site_name`

测试的话就重复3和4
