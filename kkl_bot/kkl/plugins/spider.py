# -*- coding:utf-8 -*-
import nonebot
from nonebot import on_command, CommandSession, permission as perm
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'plus'))
import re
import requests
import jjcsearch
from random import randint
from google_translate import translate, ref_words
import datetime as dt
import jianfan
import json
import kkl_config
master=kkl_config.master

new_switch,hbook_switch,jjcsearch_switch=True,True,True
@on_command('switch', aliases=('开启','关闭'), only_to_me=False) 
async def switch(session: CommandSession):
    if session.ctx['user_id'] in master:
        comman = session.ctx['raw_message'].split(' ',1)
        swtich = comman[0]#获取关键词
        plugins = comman[1]
        global new_switch,hbook_switch,hpic_switch,jjcsearch_switch
        if swtich=='开启':
            if plugins == '新闻':
                new_switch = True
            elif plugins == 'jjc':
                jjcsearch_switch= True
            elif plugins == '本子':
                hbook_switch = True
            else :
                await session.send('指令有误!')
        else :
            if plugins == '新闻':
                new_switch = False
            elif plugins == 'jjc':
                jjcsearch_switch= False
            elif plugins == '本子':
                hbook_switch = False
            else :
                await session.send('指令有误!')
        await session.send('更改完成！')
    else:
        await session.send('您配吗？')


@on_command('Rnews', aliases=('日服新闻','日服活动'), only_to_me=True)
async def Rnews(session: CommandSession):
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    url = 'https://priconne-redive.jp/news/'
    data = requests.get(url,headers = header)

    pattern_title = '<h4>(.*?)</h4>'#标题
    title = re.findall(pattern_title,data.text)

    pattern_link = '<a href="(.*?)">'#链接
    link0 = re.findall(pattern_link,data.text)
    link = [link0[i] for i in range(len(link0)) if 'new' in link0[i]]
    del(link[0],link[-1])

    pattern_time = '<time class="time">(.*?)</time>'#发布时间
    time = re.findall(pattern_time,data.text)

    msg0 = '已为骑士君查询最新{}条新闻：'.format(len(title))
    for i in range(len(title)):
        msg = (f'\n-----------------------------------------------\nNews {i+1}:\n标题: {title[i]}\n链接: {link[i]}\n时间: {time[i]}')
        msg0 += msg
    await session.send(message= msg0)

@on_command('Tnews', aliases=('台服新闻',), only_to_me=True)
async def Tnews(session: CommandSession):
    url = 'http://www.princessconnect.so-net.tw/news'
    header ={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    data = requests.get(url,headers = header).text
    #标题
    pattern_title = '<a href="/news/newsDetail/.*?">(.*?)</a>'#标题
    title = re.findall(pattern_title,data)
    #链接
    pattern_link = '<a href="/news/(.*?)\\"'
    link0 = re.findall(pattern_link,data)
    link = [f'http://www.princessconnect.so-net.tw/news/{i}' for i in link0]
    #发布时间
    pattern_time = '(.*?)<span class=".*?">'
    time0= re.findall(pattern_time,data)
    time = [i.strip() for i in time0]
    msg0 = '已为骑士君查询最新{}条新闻：'.format(len(title))
    for i in range(len(title)):
        msg = (f'\n-----------------------------------------------\nNews {i+1}:\n标题: {title[i]}\n链接: {link[i]}\n时间: {time[i]}')
        msg0 += msg
    await session.send(message= msg0)

@on_command('Tevents', aliases=('台服活动',), only_to_me=True)
async def Tevents(session: CommandSession):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get('https://pcredivewiki.tw/static/data/event.json',headers = header)
    event_pattern = '{\r\n    "campaign_name" : "(.*?)",\r\n    "start_time" : "(.*?)",\r\n    "end_time" : "(.*?)",\r\n    "type" : ".*?"\r\n  }'
    data = re.findall(event_pattern,response.text)
    n=dt.datetime.now()
    msg0 = '已查询到以下活动：'
    for i,j,k in data:
        t=dt.datetime.strptime(k,'%Y/%m/%d %H:%M')
        if t>n:
            msg=(f'\n-----------------------------------------------\n活动名称：{jianfan.toSimpleString(i)}\n活动时间：{j[5:]}--{k[5:]}')
            msg0+=msg
    await session.send(message= msg0)


@on_command('jjcsearch', aliases=('jjc查询','JJC查询','怎么拆','怎么解'), only_to_me=False)                 #changed
async def jjcs(session: CommandSession):
    if ' ' in session.ctx['raw_message'] and jjcsearch_switch: 
        result = jjcsearch.total(session.ctx['raw_message'],session.ctx['user_id'])
        await session.send(result)

@on_command('ja_to_zh', aliases=('日语翻译',), only_to_me=False)                 #changed
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='zh-CN', source='ja')
        if re_msg[0]!='' and re_msg[0]!=msg:
            await session.send(re_msg[0])

@on_command('ja_to_en', aliases=('英语翻译',), only_to_me=False)                 #changed
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='zh-CN', source='en')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_ja', aliases=('翻译日语',), only_to_me=False)                 #changed
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='ja', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_en', aliases=('翻译英语',), only_to_me=False)                 #changed
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='en', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])


@on_command('hbook', aliases=('本子查询','找本子'), only_to_me=False)
async def hbooks(session: CommandSession):
    if ' ' in session.ctx['raw_message'] and hbook_switch: 
        f_msg = session.ctx['raw_message'].split(' ',1)[1]#获取关键词
        f_type = session.ctx['message_type']
        f_qq = session.ctx['user_id']
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        keyword={'show':'title,titleen,tags','keyboard':f_msg}
        responce = requests.post('https://b-upp.com/search/',headers = header,data = keyword)
        if '没有搜索到相关的内容' in responce.text:
            n_msg='可可萝没有找到关键词[{}]相关的本子哦'.format(f_msg)
            await session.send(message=n_msg)
        else:
            p = '<a href="(.*?)" target="_blank" title="(.*?)">'
            data = re.findall(p,responce.text)
            n = len(data)
            if f_type == 'group':
                limit=3
            elif f_type == 'private':
                limit=10
            if n > limit:
                n = limit
            msg=f'已查询到{n}本关键词为[{f_msg}]的本子：'
            if f_type == 'group':
                msg=f'[CQ:at,qq={f_qq}]\n已查询到{n}本关键词为[{f_msg}]的本子：'
            for i in range(n):
                msg0 = ('\n-----------------------------------------------\n本子链接：https://b-upp.com%s \n本子标题：%s '%(data[i]))
                msg+=msg0
            await session.send(message=msg)


@on_command('anime_search', aliases=('以图搜番','这是什么番','搜番','什么番','番剧查询','这是什么动漫','动漫查询','搜动漫','什么动漫'), only_to_me=False)
async def anime_search(session: CommandSession):
    p='\\[CQ\\:image\\,file\\=.*?\\,url\\=(.*?)\\]'
    img=re.findall(p,str(session.ctx['message']))
    url=f'https://trace.moe/api/search?url={img[0]}'
    r = requests.get(url)
    if r.status_code==200:
        data=json.loads(r.text)
        d={}
        for i in range(len(data['docs'])):
            if data['docs'][i]['title_chinese'] in d.keys():
                d[data['docs'][i]['title_chinese']][0]+=data['docs'][i]['similarity']
            else:
                m=data['docs'][i]['at']/60
                s=data['docs'][i]['at']%60
                if data['docs'][i]['episode']=='':
                    n=1
                else:
                    n=data['docs'][i]['episode']
                d[jianfan.toSimpleString(data['docs'][i]['title_chinese'])]=[data['docs'][i]['similarity'],f'第{n}集',f'{int(m)}分{int(s)}秒处']
        result=sorted(d.items(),key=lambda x:x[1],reverse=True)
        t=0
        msg0=f'为骑士君按相似度找到以下{len(d)}个动漫：'
        for i in result:
            t+=1
            msg=(f'\n-----------------------------------------------\n({t})\n相似度：{i[1][0]}\n动漫名：《{i[0]}》\n时间点：{i[1][1]} {i[1][2]}')
            msg0+=msg
        await session.send(msg0)
    else :
        print(r)
        await session.send('在下太忙啦，过会再来问吧')

