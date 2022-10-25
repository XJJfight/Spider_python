import requests
from lxml import etree
import os
'''
-xpath解析原理：
    1.实例化一个etree对象，且需要将被解析的页面源码数据加载到改对象中
    2.调用etree对象中的xpath方法结合xpath表达式实现标签的定位和内容的捕获
-如何实例化一个etree对象
    1.将本地的html文档中的源码数据加载到etree对象中
    etree.parse(filepath)
    2.可以将从互联网获取的页面源码数据加载到该对象中
    etree.HTML('page_text')
    etree.XML() ->html是xml的一个子集
    3.xpath('xpath表达式')
-xpath表达式
    / : 表示的是从根节点开始定位。表示的是一个层级。
    // : 表示多个层级，可以表示从任意位置开始定位
    属性定位：//tag[@attrName="attrVakey"] atrrName:属性标签 atrrVakey:属性值
    索引定位: //tag[@attrName="key"]/tag2[i] 索引是从1开始的
    取文本：/text():读取标签的直系文本
            //text(): 获取标签中非直系的文本内容（所有内容）
    取属性：/@attrName 
            如<img src="http://www.baidu.com/meinv.jpg" alt="" /> 用/img/@src 爬取图片地址
'''
def test():
    #实例化好了一个etree对象，且将被解析的源码加载到了该对象中
    tree=etree.parse('test.html')#本地文件用parse，网页用html
    r=tree.xpath('/html/head/title')#从根节点or根目录开始层级遍历,返回一个列表，存储我们定位到标签的对象，该对象存储着文本内容
    r2=tree.xpath('//div')#遍历多个层级到div，从任意位置寻找div标签
    r3=tree.xpath('//div[@class="song"]')#属性定位
    r4=tree.xpath('//div[@class = "song"]/p[3]')#再定位到这里面的p标签,同时是第三个标签
    r5=tree.xpath('//div[@class = "tang"//li[5]/a/text()')[0]#用text读取文本，返回列表，按下标0开始读取
    r6 = tree.xpath('//div[@class = "tang"//li[5]/a//text()')[0]#获取非直系文本
    r7=tree.xpath('//div[@class="song"/img/@src')#获取属性数据（例如图片网址等）

def _58tongcheng():
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
    }
    url1 = 'https://gz.58.com/zufang/'
    page_text = requests.get(url=url1, headers=header1).text

    # 数据解析
    etree1 = etree.HTML(page_text)
    house_list = etree1.xpath('//li[@class="house-cell "]')

    fp = open('58.txt', 'w', encoding='utf-8')
    for li in house_list:
        # 局部解析
        title = li.xpath('./div[@class="des"]/h2/a/text()')[0] #./代表li变量
        new_title = ''.join(str(title).split())

        room = li.xpath('./div[@class="des"]/p/text()')[0]
        new_room = ''.join(str(room).split())

        price = li.xpath('./div[@class="list-li-right"]/div[@class="money"]/b/text()')[0]

        # 存储
        fp.write(new_title + '\n' + new_room + '\n' + str(price) + '元/月' + '\n\n')

def _4kpic():
    url='http://pic.netbian.com/4kmeinv/'
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
    }
    response=requests.get(url=url,headers=header1)
    page_text=response.text
    tree=etree.HTML(page_text)
    li_list=tree.xpath('//div[@class="slist"]/ul/li')
    if not os.path.exists('./picLibs'):
        os.makedirs('./picLibs')
    for li in li_list:
        img_src='http://pic.netbian.com'+li.xpath('./a/img/@src')[0]#图片网址
        img_name=li.xpath('./a/img/@alt')[0]+'.jpg'
        #通用处理中文乱码的解决方案
        img_name=img_name.encode('iso-8859-1').decode('gbk')
        img_data=requests.get(url=img_src,headers=header1)
        img_path='./picLibs'+img_name
        with open(img_path,'wb') as fp:
            fp.write(img_data)
def test():
    file_path='./jiang.txt'
    fp=open(file_path,'w')
    url='http://www.jinghuajt.com/xiezuozhidao/579492/'
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
    }
    response=requests.get(url=url,headers=header1)
    page_text=response.text
    tree=etree.HTML(page_text)
    p_list=tree.xpath('//div[@class="content1"]/p/text()')
    x=1
    for item in p_list:
        items=item.replace('\u3000','')
        fp.write(items)
        if x!=3:
            continue
        else:
            x+=1
            fp.write('\n')
    print(p_list)


