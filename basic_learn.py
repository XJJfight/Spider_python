import requests
import json

'''
最基础的模型
url、header信息
requests获得网页数据
数据永久存储
'''

def work1():
    # 利用爬虫代码爬去百度首页
    # 指定URL
    url = 'https://www.baidu.com'
    # 进行UA伪装，模拟浏览器,注意要将相应的User-Agent封装在一个字典中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    # 向服务器发起请求,get方法返回一个响应对象
    response = requests.get(url=url, headers=headers)
    # 获取字符串类型的响应数据
    page_text = response.text
    # 持久化存储，写入文件
    with open('./baidu.html', 'w', encoding='utf8') as fp:
        fp.write(page_text)
    print('百度首页爬取成功!!!')


def work2():
    # 利用爬虫代码爬去360搜索二舅的第一面
    # 指定URL
    url = 'https://www.sogou.com/web'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    param = {
        'query': '二舅'
    }
    # 向服务器发起请求,get方法返回一个响应对象
    response = requests.get(url=url, params=param, headers=header)
    response.encoding = 'utf-8'
    # 获取字符串类型的响应数据
    page_text = response.text
    # 持久化存储，写入文件
    with open('./360_erjiu.html', 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print('360搜索二舅首页爬取成功!!!')


# post请求、参数、json数据存储处理
def w1():
    url1 = 'https://fanyi.baidu.com/sug'
    kw = input('请输入要翻译的词')
    data1 = {
        'kw': kw  # 要翻译的词
    }
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response = requests.post(url=url1, data=data1, headers=header1)
    fanyi_json = response.json()
    FileName = kw + '.json'
    # 保存数据
    with open(FileName, 'w', encoding='utf-8') as f:
        json.dump(fanyi_json, fp=f, ensure_ascii=False)
    print('翻译完毕')


def w2():
    url1 = 'https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=0&limit=20'
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    movie_json = []
    for i in range(0, 100, 20):
        param1 = {
            'type': '24',
            'interval_id': '100:90',
            'action': '',
            'start': i,
            'limit': '20'
        }
        movie = requests.get(url=url1, params=param1, headers=header1)
        movie_json += movie.json()
        movie.close()
    with open('./movie.json', 'w', encoding='utf-8') as f:
        json.dump(movie_json, fp=f, ensure_ascii=False)
    print('电影榜单爬取完毕')

def KFC():
    url1 = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    head1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70'
    }

    cityname = input('请输入城市名字：')

    keyword = input('请输入关键字：')

    param = {
        'cname': cityname,
        'pid': ' ',
        'keyword': keyword,
        'pageIndex': '1',
        'pageSize': '10'
    }

    resp = requests.get(url=url1, headers=head1, params=param)

    rest = resp.text

    with open('RestaurantAddress.json', 'w', encoding='utf-8') as f:
        json.dump(rest, fp=f, ensure_ascii=False)

    print('爬取完毕')