import requests
from bs4 import BeautifulSoup
import lxml
'''
#soup.tagName :返回的是文档中第一次出现的tagName对应的标签
#soup.find()  : find('tagName')等同于soup.div
#               -属性定位 soup.find('div',class_/id/attr='song')
#soup.find_all('tagName'):返回符合要求的所有标签（列表）
#soup.select('某种选择器（id，class,标签。。。选择器),返回一个列表
#       ——层级选择器 soup.select('.tang>ul>li>a')[0]在class=tang中的ul标签中的li标签中选择a开头的信息，返回所有符合情况的一个列表
#                                                   大于号表示一个层级，空格则表示多个层级，等价于'.tang>ul a'
#获取标签之间的文本数据：soup.a.text/string/get_text()
#           text/get_text()可以获取某一个标签中所有的文本内容
#           string: 只可以获取该标签下面直系的文本内容
#获取标签中的属性值： soup.a['herf']
'''

 #爬取三国演义小说所有的章节标题和章节内容
#对首页的页面数据进行爬取
header1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
}
url1 = 'https://www.shicimingju.com/book/sanguoyanyi.html'

page_data = requests.get(url=url1, headers=header1)
page_data.encoding = "utf-8"

soup = BeautifulSoup(page_data.text, 'lxml')

li_list = soup.select('.book-mulu > ul > li')

#print(li_list)

fp = open('./sanguoyanyi.txt', 'w', encoding='utf-8')
for li in li_list:
    title = li.a.string #此处从li.a获得章节的标题

    content_url = 'http://www.shicimingju.com' + li.a['href']
    content_page = requests.get(url=content_url, headers=header1)
    content_page.encoding = "utf-8"

    content_soup = BeautifulSoup(content_page.text, 'lxml') #解析出对应的内容
    content_tag = content_soup.find('div', class_='chapter_content')
    content = content_tag.text
    # content.replace("&nbsp;",'\t')
    fp.write(title + ':' + content + '\n')
    print(title, '爬取成功')

