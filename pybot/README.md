## 环境

进入python环境

    ./enter-python-environment.sh 

pip安装依赖，保存路径已改成`.local`

    pip install -r requirements.txt

## dokuwiki API

文档：

http://python-dokuwiki.readthedocs.io/en/latest/

wiki的url和账号密码在`config/mywiki.py`中设置

## Google Sheets

新增了从Google Sheets获取数据的功能

### Quickstart

原文： https://developers.google.com/sheets/api/quickstart/python

先去下面的网址创建项目，获取客户端ID和密钥

https://console.developers.google.com/flows/enableapi?apiid=sheets.googleapis.com

下载到包含客户端ID和密钥的JSON，重命名为`client_secret.json`，置于当前目录下

第一次运行需要获取token，由于我们使用了虚拟环境，因此脚本后面还要添加一个参数`--noauth_local_webserver`

比如`python push_enemy_data.py --noauth_local_webserver`，执行后终端中会提供一个链接，打开此链接，授权允许，网页上会提供一串验证码，粘贴进终端后完成验证，目录下生成一个`credentials.json`文件，有了这个文件后就不用加上述参数了

### 配置

`config/enemy_sheet.py`中填写sheet id等信息
