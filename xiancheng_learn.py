import requests
from lxml import etree
import csv
import asyncio
#多线程
from threading import Thread
'''
    fun是一个方法，需要传入参数，args则是参数，为元组形式，单参数一定要留一个逗号
    T1=Thread(target=fun,args=('aa',))
'''
#多进程
from multiprocessing import Process
#线程池：一次性开辟一些线程，我们用户直接给线程池子提交任务，线程任务的调度交给线程池来完成

'''
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor #线程池、进程池

def fn(name):
    for i in range(1000):
        print(name,i)

def main():
    #创建线程池,50个线程
    with ThreadPoolExecutor(50) as t:
        for i in range(100):
            t.submit(fn,name=f"线程{i}")
    #等待线程池中的任务全部执行完毕，才继续执行（守护）
    print("123")

def download_one_page(page):
    url='http://www.xinfadi.com.cn/getPriceData.html'
    data1={
        'limit': '20',
        'current': page
    }
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
    }
    #拿到页面源代码
    resp=requests.post(url,data=data1,headers=header1)
    page_json=resp.json()
    f = open("./data.xlsx", mode='a', encoding='utf-8')
    csvwriter = csv.writer(f)
    for item in page_json['list']:
        csvwriter.writerow(item.values())
    f.close()
    print(f'第{page}页提取完毕')

def caijia():
    #1.如何提取单个页面数据
    #2.上线程池，多个页面同时抓取
    with ThreadPoolExecutor(50) as t:
        for i in range(2,200):
            t.submit(download_one_page,f'{i}')

'''

'''
一般情况下，当程序处于IO工作时候，线程处于阻塞状态
协程：当程序遇见IO操作时，可以选择性的切换到其他任务上
在单线程的条件下，多任务异步操作

async def func1():
    #一堆操作
    #time.sleep(3) #当程序出现了同步操作的时候（sleep),异步就中断了
    #应该用：
    await asyncio.sleep(3)     #await是挂起
async def func2():
    #一堆操作
async def func3():
    #一堆操作
async def main():
    f1=func1() #此时的函数是异步协程函数，得到一个协程对象
    如果警告，则要手动包装成task对象
    asyncio.create_task(func1())
    f2=func2()
    f3=func3()
    task=[f1,f2,f3]
    #一次性启动多个任务（协程）
    await asyncio.wait(task)

#上述程序启动
if __name__=='__main__':
    t1=time.time()
    asyncio.run(main())
    t2=time.time()
'''

'''
#应用于爬虫
async def download(url):
    print('准备开始下载')
    await asyncio.sleep(2) #网络请求一堆过程，伪代码
    print('下载完成')

async def main():
    urls=[
        'http://www.baidu.com',
        'http://www.bilibili.com',
        'http://www.163.com'
    ]

    tasks=[]
    for url in urls:
        d=download(url)
        tasks.append(d)

    await asyncio.wait(tasks)

if __name__=='__main__':
    asyncio.run(main())
'''

'''通用模板
#requests.get() 同步的代码->异步操作aiohttp
import aiohttp
import asyncio

urls=[
    'http://kr.shanghai-jiuxin.com.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg',
    'http://kr.shanghai-jiuxin.com.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg',
    'http://kr.shanghai-jiuxin.com.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg',
]

async def aiodownload(url):
    file_name=url.rsplit('/',1)[1] #获取图片名
    async with aiohttp.ClientSession() as session:#相当于requests  requests.get()== s.get() , requests.post()==s.post()
        async with session.get(url) as resp:
            #resp.content.read()  ==resp.content
            #resp.text() ==resp.text
            #resp.json() == resp.json()
            #可以学习aiofiles进行文件读写的异步
            with open(file_name,mode='wb') as f:
                f.write(await resp.content.read())  #读取内容是异步的，需要await挂起
    print(file_name,'搞定')

async def main():
    tasks=[]
    for url in urls:
        tasks.append(aiodownload(url))
    await asyncio.wait(tasks)

if __name__=='__main__':
    asyncio.run(main())
'''

#爬小说
#https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"}  #->所有章节名称
#https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1} #小说的具体内容

import requests
import asyncio
import aiohttp
import json
import aiofiles
'''
1.同步操作：访问getCatalog拿到所有章节的cid和名称
2.异步操作：访问getChapterContent下载所有文章内容
'''
async def aiodownload(cid,b_id,title):
    data={
        "book_id": b_id,
        "cid":f"{b_id}|{cid}",
        "need_bookinfo": 1  # 小说的具体内容
    }
    data=json.dumps(data)
    url=f'https://dushu.baidu.com/api/pc/getChapterContent?data={data}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic=await resp.json()
            async with aiofiles.open('./novel/'+dic['data']['novel']['chapter_index']+' '+title+'.txt',mode='w',encoding='utf-8') as f:
                await f.write(dic['data']['novel']['content'])  #把小说内容写出
async def getCatalog(url,b_id):
    resp=requests.get(url)
    dic=resp.json()
    tasks=[]
    for item in dic['data']['novel']['items']: #item就是对应每一个章节的名称和cid
        title=item['title']
        cid=item['cid']
        print(title+'的cid:'+cid+'已获得')
        #准备异步任务
        tasks.append(aiodownload(cid,b_id,title))
    await asyncio.wait(tasks)

if __name__ =='__main__':
    book_id='4306063500'
    url='https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+book_id+'"}'
    asyncio.run(getCatalog(url,book_id))

