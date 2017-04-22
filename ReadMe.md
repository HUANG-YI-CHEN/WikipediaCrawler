# Wikipedia Crawler
* 抓取維基百科`名稱空間`中`類別`、`中文名稱`、`英文名稱`、`名稱空間別名關聯`
* 抓取維基百科`語言列表`中`代碼`、`中文名稱`、`中文名稱`、`地方名稱`
* 抓取維基百科`條目`中`條目編號`、`條目名稱`、`條目顯示標題`、`條目摘要`、`條目內容`、`條目別名關聯`、`條目相關資訊` ，關於`條目相關資訊`以 `JSON` 格式儲存

## 命名空間 Namespace ( 類別, 中文, 英文 )
Result : 
 ![](http://imgur.com/a/Um7k2)

## 語言列表 Language ( 語言編號, 中文, 英文, 地方名稱, 代碼 )
Result : 
 ![](http://imgur.com/a/hBrMt)

## 條目 Object (條目編號, 條目顯示名稱, 條目名稱, 摘要, 條目內容, 有條目內容, 有條目別名 )
Result : 
 ![](http://imgur.com/a/PDw9N)

## 條目繼承 Wikiepdia ( 條目編號, 條目名稱, 條目JSON文件 )
Result : 
 ![](http://imgur.com/a/zt06V)


# Getting Started
## 系統需求
* Python 3+

## 安裝套件
* pip install requests pymssql psycopg2 configparser beautifulsoup4 --upgrade pip

## 設定檔
建立設定檔 config.ini 放置於專案根目錄下
* config.ini 內容如下 :

> [database]

>> hostname=localhost

>> username=

>> password=

>> database=


## 程式執行
`不加參數` ： 進入程式執行後，會提醒輸入  選取 `MODE` 執行 [1] 條目空間 [2] 語言列表 [3] 條目空間/語言列表 [4] 條目 [5] 離開
```
python main.py
```
`加入參數` : 進入程式執行後，直接執行程序抓取`條目編號` 1 -> 10000
```
python main.py 1 10000
```

## 後續補充
待續......


