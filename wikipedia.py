#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
import requests
import json
import time
import random
from bs4 import BeautifulSoup
from lib.config import Config
from lib.connect2sql import MSSQL

clear = lambda: os.system('cls')
unicode_cmd = lambda: os.system('chcp 65001 &')
"""
Python3 寫一個網路爬蟲
http://marsray.pixnet.net/blog/post/61040521-%5Bpython3%5D-%E7%94%A8-python3-%E5%AF%AB%E4%B8%80%E5%80%8B%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2
Python3中如何得到Unicode碼對應的中文
https://www.zhihu.com/question/26921730
# print (response.content.decode("utf-8"))
# print (response.text.encode("latin1").decode("utf-8"))
"""
def sqltest():
    config = Config().getCfg( 'database' )
    db_connect = MSSQL( hostname=config['hostname'], username=config['username'], password=config['password'], database=config['database'] )
    sql = "select top 1 * from Language"
    results = db_connect.ExecQuery( sql )
    db_connect.Close()

def timetest():
    start = time.time()
    print('Start : %.4f'%( start ))
    time.sleep( random.uniform(1, 5) )
    end = time.time()
    print ('End : %.4f'%( end ))
    print ('Cost : %.4f'%( abs(end-start) ))

def parserURL(url):
    url = urllib.parse.unquote(url)
    Scheme = url[:url.index('://')]
    Hostname = url[url.index('://')+len('://'):][:url[url.index('://')+len('://'):].index('/')]
    Path = url[url.index(Hostname)+len(Hostname):]    
    return {'URL':url,'Scheme':Scheme,'Hostname':Hostname,'Path':Path}

def replaceDeilimeter( word ):
    word = word.replace('\'','\'\'')
    return (word)

def replaceHtml( word ):
    word = word.replace('&quot;','\"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&nbsp;',' ')
    return (word)

def replaceHtmlTag( word ):
    word = BeautifulSoup( word, 'html.parser' )
    return (word.text)

def namespace():
    """
    https://zh.wikipedia.org/w/api.php?action=query&format=json&meta=siteinfo&siprop=namespaces|namespacealiases
    """    
    options = {
        'url': 'https://zh.wikipedia.org/w/api.php',
        'headers': { 
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'cache-control':'max-age=0',
            'cookie':'GeoIP=TW:TXG:Taichung:24.14:120.68:v4; CP=H2; WMF-Last-Access=12-Apr-2017; WMF-Last-Access-Global=12-Apr-2017; TBLkisOn=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3047.0 Safari/537.36',
            'content-type':'application/json; charset=utf-8'
        },
        'params': {
            'action': 'query',
            'format': 'json',
            'meta': 'siteinfo',
            'siprop': 'namespaces|namespacealiases'
        }
    }    
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001')
    content = json.loads( content )['query']
    namespaces = content['namespaces'] # number => id , content|canonical, *
    namespaceAliases = content['namespacealiases'] # id, *

    dicts = {'namespaces':[],'namespaceAliases':[]}
    for i in namespaces:
        try:
            dicts['namespaces'].append( {'type':namespaces[i]['id'], 'cname':namespaces[i]['*'], 'ename':namespaces[i]['content'] } )
        except:
            dicts['namespaces'].append( {'type':namespaces[i]['id'], 'cname':namespaces[i]['*'], 'ename':namespaces[i]['canonical'] } )
    for i in namespaceAliases:
         dicts['namespaceAliases'].append( {'type':i['id'], 'cname':i['*'] } )
    return (dicts)

def language():
    """
    https://zh.wikipedia.org/w/api.php?format=json&action=query&meta=siteinfo&siprop=interwikimap&sifilteriw=local
    https://zh.wikipedia.org/w/api.php?action=query&format=json&meta=siteinfo&siprop=languages
    https://zh.wikipedia.org/w/api.php?action=query&format=json&meta=siteinfo&siprop=languages&siinlanguagecode=zh-tw
    https://zh.wikipedia.org/w/api.php?action=query&format=json&meta=siteinfo&siprop=languages&siinlanguagecode=en
    """    
    options = {
        'url': 'https://zh.wikipedia.org/w/api.php',
        'headers': { 
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'cache-control':'max-age=0',
            'cookie':'gsScrollPos=; CP=H2; GeoIP=TW:TXG:Taichung:24.14:120.68:v4; WMF-Last-Access=20-Apr-2017; WMF-Last-Access-Global=20-Apr-2017; TBLkisOn=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3047.0 Safari/537.36'
        },
        'params': {
            'action': 'query',
            'format': 'json',
            'meta': 'siteinfo',
            'siprop': 'languages',
            'siinlanguagecode': ''
        }
    }    
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001') 
    content = json.loads( content )['query']
    languages = content['languages']
    dicts = {'languages':[]}
    for i in languages:
         dicts['languages'].append( {'code':i['code'], 'lname':i['*'], 'cname':'', 'ename':'' } )
    options['params']['siinlanguagecode'] = 'zh-tw'
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001') 
    content = json.loads( content )['query']
    languages = content['languages']
    for i in languages:
        for j in range(len(dicts['languages'])):
            if dicts['languages'][j]['code'] == i['code']:
                dicts['languages'][j]['cname'] = i['*']
                break
    options['params']['siinlanguagecode'] = 'en'
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001') 
    content = json.loads( content )['query']
    languages = content['languages']
    for i in languages:
        for j in range(len(dicts['languages'])):
            if dicts['languages'][j]['code'] == i['code']:
                dicts['languages'][j]['ename'] = i['*']
                break
    return (dicts)

def redirects( pageid = None, title = None ):
    """
    https://zh.wikipedia.org/wiki/Special:ApiSandbox
    https://zh.wikipedia.org/w/api.php?format=json&action=query&prop=redirects&redirects=1&titles=斐迪南
    https://zh.wikipedia.org/w/api.php?format=json&action=query&prop=redirects&redirects=1&pageids=13
    """    
    options = {
        'url': 'https://zh.wikipedia.org/w/api.php',
        'headers': { 
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'cookie':'CP=H2; WMF-Last-Access=21-Apr-2017; WMF-Last-Access-Global=21-Apr-2017; GeoIP=TW:TXG:Taichung:24.14:120.68:v4; TBLkisOn=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        },
        'params': {
            'format': 'json',
            'action': 'query',
            'prop': 'redirects',
            'redirects':'1',
            'pageids':'',
            'titles':''
        }
    }    
    if pageid is not None and title is None:
        options['params'].pop('titles')
        options['params']['pageids'] = pageid
    elif pageid is None and title is not None:
        options['params'].pop('pageids')
        options['params']['titles'] = title
    else:
         raise NameError( u'pageid and title can\'t input at the same time' )
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001')
    
    content = json.loads( content )['query']
    pages = {}
    try:
        idNum = list(content['pages'].keys())[0]
        pages = content['pages'][idNum]
    except:
        pages = content['pages']

    dicts = { 'page':[], 'redirects':[], 'rel':[] }
    try:
        pages[0]['missing']
    except:
        try:
            pages['missing']
        except:
            if pages['pageid'] == pageid:
                try:
                    for i in pages['redirects']:
                        dicts['redirects'].append( { 'oid1':i['pageid'], 'type':i['ns'], 'cname': i['title'] } )
                        dicts['rel'].append( { 'oid1':pages['pageid'], 'oid2':i['pageid'] } )
                        dicts['rel'].append( { 'oid1':i['pageid'], 'oid2':pages['pageid'] } )
                    dicts['page'].append( { 'oid':pages['pageid'], 'type':pages['ns'], 'ename':pages['title'], 'ownerMID':1,'nClick': 1 } )
                except:
                    dicts['page'].append( { 'oid':pages['pageid'], 'type':pages['ns'], 'ename':pages['title'], 'ownerMID':1,'nClick': 0 } )                
            else:
                dicts['page'].append( { 'oid':pageid, 'type':pages['ns'], 'ename':'', 'ownerMID':0,'nClick': 1 } )

    return (dicts)

def summary( pageid = None, title = None ):
    """
    https://zh.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&redirects=1&explaintext=&exsectionformat=wiki&pageids=13
    """    
    options = {
        'url': 'https://zh.wikipedia.org/w/api.php',
        'headers': {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'cookie':'CP=H2; WMF-Last-Access=21-Apr-2017; WMF-Last-Access-Global=21-Apr-2017; GeoIP=TW:TXG:Taichung:24.14:120.68:v4; TBLkisOn=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        },
        'params': {
            'format': 'json',
            'action': 'query',
            'prop': 'extracts',
            'redirects':'1',
            'exintro':'1',
            'explaintext':'1',
            'exsectionformat':'wiki',
            'pageids':'',
            'titles':''
        }
    }
    if pageid is not None and title is None:
        options['params'].pop('titles')
        options['params']['pageids'] = pageid
    elif pageid is None and title is not None:
        options['params'].pop('pageids')
        options['params']['titles'] = title
    else:
         raise NameError( u'pageid and title can\'t input at the same time' )
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001')

    content = json.loads( content )['query']
    pages = {}
    try:
        idNum = list(content['pages'].keys())[0]
        pages = content['pages'][idNum]
    except:
        pages = content['pages']

    dicts = { 'summary':[], 'article':[] }
    try:
        pages[0]['missing']
    except:
        try:
            pages['missing']
        except:
            dicts['summary'] = replaceHtml( pages['extract'] )
    
    options['params'].pop('exintro')
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001')

    content = json.loads( content )['query']
    idNum = list(content['pages'].keys())[0]
    pages = content['pages'][idNum]
    try:
        pages[0]['missing']
    except:
        try:
            pages['missing']
        except:
            dicts['article'] = replaceHtml( pages['extract'] )
    return (dicts)

def pageParse( pageid = None, title = None ):
    """
    https://zh.wikipedia.org/w/api.php?format=json&action=parse&pageid=13
    """    
    options = {
        'url': 'https://zh.wikipedia.org/w/api.php',
        'headers': { 
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'cookie':'CP=H2; WMF-Last-Access=21-Apr-2017; WMF-Last-Access-Global=21-Apr-2017; GeoIP=TW:TXG:Taichung:24.14:120.68:v4; TBLkisOn=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        },
        'params': {
            'format': 'json',
            'action': 'parse',
            'pageid':'',
            'title':''
        }
    }
    if pageid is not None and title is None:
        options['params'].pop('title')
        options['params']['pageid'] = pageid
    elif pageid is None and title is not None:
        options['params'].pop('pageid')
        options['params']['title'] = title
    else:
         raise NameError( u'pageid and title can\'t input at the same time' )
    response = requests.get( url=options['url'], headers=options['headers'], params=options['params'])
    content = response.content.decode('cp65001')

    content = json.loads( content )
    try:
        content['error']
    except:
        content = content['parse']  #pageid, title, displaytitle, text ,langlinks: #lang->code, #*->title, links: #ns->type, #*->cname, templates: #ns->type, #*->cname, images, externallinks, sections, 
        content['displaytitle'] = replaceHtmlTag( content['displaytitle'] )
    return (content)

def pageFormat( pageid = None, title = None ):
    if pageid is not None and title is None:
        pageid = pageid
        title = None
    elif pageid is None and title is not None:
        pageid = None
        title = title
    else:
         raise NameError( u'pageid and title can\'t input at the same time' )

    dicts = { 'page':[], 'extra':[] }
    
    redirect = redirects( pageid ) if pageid is not None else redirects( title ) 
    if not redirect['page']:
        pass
    else:
        page = pageParse( pageid = pageid ) if pageid is not None else pageParse( title = title )
        dicts['page'].append( redirect['page'][0] )
        dicts['page'][0].setdefault( 'cname', page['displaytitle'] )
        dicts['page'][0]['ename'] = page['title']
        if dicts['page'][0]['OwnerMID'] == 1 :
            text = summary( pageid ) if pageid is not None else summary( title )
            dicts['page'][0].setdefault( 'cdes', text['summary'] )
            dicts['page'][0].setdefault( 'edes', text['article'] )
            try:
                page.setdefault('redirects', redirect['redirects'] )
                page.setdefault('rel', redirect['rel'] )
            except:
                pass
            dicts['extra'].append( page )
    return (dicts)

def namespaceImport( db_connect ):
    namespaces = namespace()['namespaces']
    namespaceAliases = namespace()['namespaceAliases']

    createTB = """
                if exists ( select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = \'dbo\' and TABLE_NAME = N\'NRel\' )
                    drop table NRel
                 
                if exists ( select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = \'dbo\' and TABLE_NAME = N\'Namespace\' )
                    drop table Namespace
                
                create table Namespace(
                    NID int identity(1,1) not null primary key clustered,
                    Type int,
                    CName nvarchar(50) null unique nonclustered,
                    EName nvarchar(50) null
                )             
                create table NRel(
                    NID1 int not null,
                    NID2 int not null,
                    MG int null,
                    Rank int null,	
                    Des nvarchar(255),
                    constraint FK_NRel_NID1 foreign key(NID1) references Namespace(NID),
                    constraint FK_NRel_NID2 foreign key(NID2) references Namespace(NID),
                    constraint PK_NRelID primary key(NID1, NID2)
                )
                """
    db_connect.ExecNonQuery( createTB )

    for i in namespaces:
        insert = """
                set identity_insert Namespace on
                insert into Namespace( NID, Type, CName, EName) values( %d, %d, N\'%s\', N\'%s\' )
                set identity_insert Namespace off
                """%( i['type'], i['type'], i['cname'], i['ename'] )
        db_connect.ExecNonQuery( insert )
    
    dbcc = 'dbcc checkident(\'Namespace\', reseed, 15)' 
    db_connect.ExecNonQuery( dbcc )

    for i in namespaceAliases: 
        check = db_connect.ExecQuery( 'select top 1 cname from Namespace where type = %s and cname = N\'%s\' '%( i['type'], i['cname'] ) )
        if not check :
            sel = 'select top 1 NID from Namespace where type = %s and ename is not null '%( i['type'] )
            query = db_connect.ExecQuery( sel )
            insert = """
                    declare @NID int
                    insert into Namespace( Type, CName ) values( %s, N\'%s\' )
                    set @NID = ( select @@identity )
                    insert into NRel( NID1, NID2 ) values( %d , @NID )
                    """%( i['type'], i['cname'], query[0][0] )   
            db_connect.ExecNonQuery( insert )
    print ('Namespace data insert completely ...')

def languageImport( db_connect ):
    languages = language()['languages']
    createTB = """
                if exists ( select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = \'dbo\' and TABLE_NAME = N\'Language\' )
                    drop table Language
                create table Language(
                    LID int identity(1,1) not null primary key clustered,
                    CName nvarchar(50) not null unique nonclustered,
                    EName nvarchar(50) null,
                    LName nvarchar(255) null,
                    Code nvarchar(20) null
                )
                """
    db_connect.ExecNonQuery( createTB )

    for i in languages:
        insert = ' insert into Language( CName, EName, LName, Code ) values ( N\'%s\', N\'%s\', N\'%s\', N\'%s\' ) '%( replaceDeilimeter(i['cname']), replaceDeilimeter(i['ename']), replaceDeilimeter(i['lname']), i['code'] )
        db_connect.ExecNonQuery( insert )
    print ('Language data insert completely ...')

def pageImport( db_connect, lowerbound = None, upperbound = None ):
    if lowerbound is None:
        lowerbound = 1
    else:
        sel = ' select max(oid) from object where oid > %s and oid < %s and cname is not null '%( lowerbound, upperbound)
        query = db_connect.ExecQuery( sel )
        lowerbound = int( query[0][0] )
    if upperbound is None:
        upperbound = 6000000
    else:
        upperbound = upperbound
   
    for i in range( lowerbound, upperbound ):
        page = pageFormat( pageid = i )
        if not page['page'] :
            print ( 'oid : %07d'%( i ), 'not exists' )
        else:
            print ( 'oid : %07d'%( i ) )
            oid = 0; namespace = 0; cname = ''; cdes = ''; ename = ''; edes = '' ; ownerMID = 0; nClick = 0; jsonString = ''
            oid =  page['page'][0]['oid']
            namespace = page['page'][0]['type']
            cname = replaceDeilimeter( page['page'][0]['cname'] )            
            ename = replaceDeilimeter( page['page'][0]['ename'] )
            nClick = page['page'][0]['nClick']
            ownerMID = page['page'][0]['OwnerMID']
            if not page['extra']:
                pass
            else:
                cdes = replaceDeilimeter( page['page'][0]['cdes'] )
                edes = replaceDeilimeter( page['page'][0]['edes'] )
                jsonString = replaceDeilimeter( json.dumps( page['extra'][0] ) )                

            sel = ' select top 1 oid from object where oid = %s '%( i )
            query = db_connect.ExecQuery( sel )
            if not query:
                insert = """
                        set identity_insert object on
                        insert into Object( oid, type, cname, cdes, ename, edes, ownerMID, nclick, databyte ) values( %s, %s, N\'%s\', N\'%s\', N\'%s\', N\'%s\', %s, %s, 1 )
                        set identity_insert object off
                        set identity_insert Wikipedia on
                        insert into Wikipedia( oid, type, cname, json) values( %s, %s, N\'%s\', N\'%s\' )
                        set identity_insert Wikipedia off
                        """%( oid, namespace, cname, cdes, ename, edes, ownerMID, nClick, oid, namespace, ename, jsonString )
                
                db_connect.ExecNonQuery ( insert )

                if not page['extra']:
                    pass
                else:
                    for i in page['extra'][0]['rel']:
                        sel = ' select top 1 oid from object where oid = %s '%( i['oid1'] )
                        query = db_connect.ExecQuery( sel )
                        if not query:
                            insert = """
                                    set identity_insert object on
                                    insert into Object( oid, type) values( %s, 0)
                                    set identity_insert object off
                                    """%(i['oid1'])
                            db_connect.ExecNonQuery ( insert )
                        
                        sel = ' select top 1 oid from object where oid = %s '%( i['oid2'] )
                        query = db_connect.ExecQuery( sel )
                        if not query:
                            insert = """
                                    set identity_insert object on
                                    insert into Object( oid, type) values( %s, 0)
                                    set identity_insert object off
                                    """%(i['oid2'])
                            db_connect.ExecNonQuery ( insert )

                        sel  = ' select top 1 oid1, oid2 from ORel where oid1 = %s and oid2 = %s '%( i['oid1'], i['oid2'] )
                        query = db_connect.ExecQuery( sel )
                        if not query:
                            insert = ' insert into ORel( oid1, oid2, Des ) values ( %s, %s, \'alias\' )'%( i['oid1'], i['oid2'] )
                            db_connect.ExecNonQuery ( insert )
            else:
                update = """
                        update Object set type = %s, cname =  N\'%s\', cdes =  N\'%s\',  ename =  N\'%s\', edes =  N\'%s\', ownerMID = %s, nClick = %s, databyte = 1 where oid = %s
                        update Wikipedia set type = %s, cname = N\'%s\', json = N\'%s\' where oid = %s
                        """%( namespace, cname, cdes, ename, edes, ownerMID, nClick, oid,  namespace, ename, jsonString, oid )
                db_connect.ExecNonQuery ( update )

def main():
    argvs = sys.argv[0:]
    cfg = Config().getCfg('database')
    sqlserver = MSSQL( hostname=cfg['hostname'],username=cfg['username'], password=cfg['password'],database=cfg['database'] )
    if len(argvs) <3:
        while True:
            clear()
            print ("""Please, choose one option to excute
            (1) create table Namespace and import data
            (2) create table Language and import data
            (3) create table Namespace / Language and import data
            (4) Object / Wikipedia Table import data
            (5) Exit                
            """,end='')
            keyin = input( u'choice : ' )
            if keyin == '1':
                namespaceImport( db_connect = sqlserver )
            elif keyin == '2':
                languageImport( db_connect = sqlserver )
            elif keyin == '3':
                namespaceImport( db_connect = sqlserver )
                languageImport( db_connect = sqlserver )
            elif keyin == '4':
                lowerbound = int(input( u'Please, input from : ' ))
                upperbound = int(input( u'Please, input to : ' ))
                pageImport( sqlserver, lowerbound, upperbound )
            elif keyin == '5':
                sys.exit()
            else:
                print('\tInput error !!!')
    else:
        lowerbound = int( argvs[1] )
        upperbound = int( argvs[2] )
        pageImport( sqlserver, lowerbound, upperbound )

    sqlserver.Close()

if __name__ == '__main__':
# 直接執行本腳本則__main__會等於__name__
    unicode_cmd()
    clear()
    main()
