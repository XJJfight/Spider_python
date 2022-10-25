#selenium 自动化测试工具
#可以打开浏览器，像人一样去操作浏览器
#需要下载浏览器驱动： https://npm.taobao.org/mirrors/chromedriver
#把解压缩的浏览器驱动放在python解释器所在文件夹

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys #模拟键盘
import time

def basic():
    #1.创建浏览器对象
    web=Chrome()
    #2.打开一个网址
    web.get('http://lagou.com')
    #定位点击位置：对网络语言直接复制xpath
    el=web.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[4]/a')
    el.click()#点击事件
    #找到搜索框，输入python，输入回车or点击搜索按钮
    time.sleep(1)#等一下让网页刷新完成
    web.find_element_by_xpath('//*[@id="search_input"]').send_keys('python',Keys.ENTER)

    #查找存放数据的
    # 位置进行数据提取
    #找到页面中存放数据的所有li
    time.sleep(1)
    li_list=web.find_elements('xpath','//*[@id="jobList"]/div[1]/div')
    for li in li_list:
        job_name=li.find_element_by_tag_name('a').text
        job_price=li.find_element_by_xpath('./div[1]/div[1]/div[2]/span').text
        company=li.find_element_by_xpath('./div[1]/div[2]/div[1]/a').text
        print(company,job_name,job_price)

def chuangkou_qiehuan():
    web = Chrome()
    web.get('http://lagou.com')
    web.find_element_by_xpath('//*[@id="cboxClose"]').click()
    time.sleep(1)
    web.find_element_by_xpath('//*[@id="search_input"]').send_keys('python', Keys.ENTER)
    time.sleep(1)
    web.find_element_by_xpath('//*[@id="jobList"]/div[1]/div[1]/div[1]/div[1]/div[1]/a').click()
    #点击产生新窗口要切换
    web.switch_to.window(web.window_handles[-1])#取最后也就是最新打开的网站

    #在新窗口中继续操作
    job_detail=web.find_element_by_xpath('//*[@id="job_detail"]/dd[2]/div').text
    print(job_detail)

    web.close()
    #关掉此窗口再回到原来窗口中
    web.switch_to.window(web.window_handles[0])
    print(web.find_element_by_xpath('//*[@id="jobList"]/div[1]/div[1]/div[1]/div[1]/div[1]/a').text)
    '''
    #如果再页面中遇到iframe如何处理
    web = Chrome()
    web.get('https://www.91kanju.com/vod-play/541-2-1.html')
    #处理iframe需先拿到iframe,然后切换视角到iframe,然后才可以拿到数据
    iframe= web.find_element_by_xpath('//*[@id="player_iframe"]')
    web.switch_to.frame(iframe)
    #web.switch_to.default_content() #切换回原页面
    tx=web.find_element_by_xpath('//*[@id="main"]/h3[1]').text
    '''

def wutouliulanqi():
    #浏览器在后台运行不显示出来，只输出数据
    #准备好参数配置(无头)
    from selenium.webdriver.chrome.options import  Options
    opt=Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    web = Chrome(options=opt)

    web.get('http://www.endata.com.cn/BoxOffice/BO/Year/index.html')
    #定位到下拉列表
    sel_el=web.find_element_by_xpath('//*[@id="OptionDate"]')
    from selenium.webdriver.support.select import Select
    #对元素进行包装，包装成下拉菜单
    sel=Select(sel_el)
    #让浏览器进行调整选项
    for i in range(len(sel.options)): #获得选项个数,i就是每一个下拉选项的索引位置
        sel.select_by_index(i) #按照索引进行切换
        time.sleep(1)
        table=web.find_element_by_xpath('//*[@id="TableList"]/table')
        print(f'第{2022-i}年')
        print(table.text) #打印所有文本信息
        print('=========================')

    #如何拿到页面代码elements（经过数据加载及js执行之后的结果的html
    web.page_source
