# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import requests
from urllib import request
from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio
import random

class Login_cookie():
    def __init__(self,name,password):
        self.cookies=None
        self.name=name
        self.password=password

    #展示图片
    async def cv_show(self,img):  # 展示图片
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 计算滑动距离
    async def get_distance(self):
        # 缺口背景图路径, 滑块图片路径
        # 转换颜色通道，保持颜色准确
        image = cv2.imread(r"image.png")
        gap = cv2.imread(r"template.png")

        image_gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
        gap_gray = cv2.cvtColor(gap.copy(), cv2.COLOR_BGR2GRAY)

        h, w = gap_gray.shape
        print(h)
        print(w)

        w_start_index, h_start_index = 0, 0
        w_end_index, h_end_index = w, h
        # 缺口图去除背景
        for i in range(h):
            if not any(gap_gray[i, :]):
                h_start_index = i
            else:
                break

        for i in range(h - 1, 0, -1):
            if not any(gap_gray[i, :]):
                h_end_index = i
            else:
                break

        for i in range(w):
            if not any(gap_gray[:, i]):
                w_start_index = i
            else:
                break

        for i in range(w - 1, 0, -1):
            if not any(gap_gray[:, i]):
                w_end_index = i
            else:
                break

        #print(h_start_index)
        #print(h_end_index)
        #print(w_start_index)
        #print(w_end_index)

        # 取出完整的缺口图
        gap_gray = gap_gray[h_start_index:h_end_index + 1, w_start_index:w_end_index + 1]
        #cv_show(gap_gray)

        image_gray = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5,
                                       0)  # 图像二值化，增强对比与特征
        gap_gray = cv2.adaptiveThreshold(gap_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 0)

        image_v1 = cv2.Canny(image_gray, 0, 500)  # 图像边缘检测
        gray_v1 = cv2.Canny(gap_gray, 0, 500)

        #cv_show(gray_v1)
        #cv_show(image_v1)

        result = cv2.matchTemplate(image_v1, gray_v1, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        x, y = max_loc
        h, w = gap_gray.shape

        result = np.array(image.copy())
        color = (0, 0, 255)
        # print(check_box)
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)

        # res = np.hstack([image_gray,gray_v1, image_v1, result])
        #cv_show(result)

        distance = x - w_start_index
        print(distance)
        return distance+8

    #获得图片
    async def get_pic_url(self,page):
        await asyncio.sleep(5)
        img_url = await page.xpath("/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img")
        img_src = await (await img_url[0].getProperty('src')).jsonValue()
        request.urlretrieve(img_src, 'image.png')
        template_src = await (await img_url[1].getProperty('src')).jsonValue()
        request.urlretrieve(template_src, 'template.png')
        #print(img_src)
        #print(template_src)

    #模拟速度
    async def slide_list(self,total_length):
        '''
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+½at²
        ③v²-v0²=2as
        :param total_length: 需要移动的距离
        :return: 每段移动的距离列表
        '''
        v = 0  # 初速度
        t = 1  # 单位时间为0.3s来统计轨迹，轨迹即0.3内的位移
        slide_result = []  # 位移/轨迹列表，列表内的一个元素代表一个T时间单位的位移,t越大，每次移动的距离越大
        current = 0  # 当前的位移
        mid = total_length * 3 / 5  # 到达mid值开始减速
        while current < total_length:
            if current < mid:
                a = 0.4  # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            else:
                a = -0.5
            v0 = v  # 初速度
            s = v0 * t + 0.5 * a * (t ** 2)  # 0.2秒时间内的位移
            current += s  # 当前的位置
            slide_result.append(round(s))  # 添加到轨迹列表
            v = v0 + a * t  # 速度已经达到v,该速度作为下次的初速度
        return slide_result

    #移动滑块
    async def sliding(self,page,total_length):
        await page.hover('.yidun_slider')
        await page.mouse.down()
        await page.waitFor(1000)
        length_list = await self.slide_list(total_length)
        for length in length_list:
            await page.mouse.move(page.mouse._x + length, page.mouse._y,
                              {'delay': random.randint(1000, 2000), 'steps': 3})
        await page.mouse.move(page.mouse._x - 1, page.mouse._y,
                          {'delay': random.randint(1000, 2000), 'steps': 3})
        await page.waitFor(1000)
        await page.mouse.up()
        await page.waitFor(1000)

    #登录程序
    async def main(self,username,password):
        home_url = 'https://www.zhihu.com/hot'
        login_url = 'https://www.zhihu.com/signin?next=%2Fhot'
        # 'headless': False  是否以”无头”的模式运行,，即是否显示窗口，默认为 True(不显示)
        # 'ignoreHTTPSErrors': True  是否忽略 Https 报错信息，默认为 False
        # 'dumpio': True  防止多开导致的假死
        # args常用配置
        #### '--no-sandbox'  取消沙盒模式，放开权限
        #### '--disable-infobars'  不显示信息栏，比如：chrome正在受到自动测试软件的控制
        #### '--window-size=1920,1080' 设置窗口大小 和"--start-maximized"参数互斥
        #### "--start-maximized"  窗口最大化
        #### "--proxy-server=http://127.0.0.1:80"  设置代理
        #### "--user-agent=Mozilla/5.0......"  设置UA
        browser = await launch(
            {'headless': False, 'dumpio': True, 'autoClose': False,
            'ignoreHTTPSErrors': True,
             'args': ['--no-sandbox', '--disable-infobars'],
            'executablePath': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            })
        page = await browser.newPage()  # 新建标签页
        await stealth(page)  # 消除指纹
        await page.evaluateOnNewDocument('''
                    () => {
                    const newProto = navigator.__proto__;
                    delete newProto.webdriver;
                    navigator.__proto__ = newProto;
                    }
                ''')
        # 设置窗口大小
        #await page.setViewport({'width': width, 'height': height})
        await page.goto(home_url)  # 前往目标网页
        await page.waitForSelector('#root > div > main > div > div > div > div > div.signQr-rightContainer > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-tabs > div:nth-child(2)',{'timeout':3000})
        await page.click('#root > div > main > div > div > div > div > div.signQr-rightContainer > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-tabs > div:nth-child(2)')
        await page.type('#root > div > main > div > div > div > div > div.signQr-rightContainer > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-account > div > label > input',username)
        await page.type('#root > div > main > div > div > div > div > div.signQr-rightContainer > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-password > div > label > input',password)
        await asyncio.sleep(5)
        await page.waitForSelector('#root > div > main > div > div > div > div > div.signQr-rightContainer > div > div.SignContainer-content > div > div:nth-child(1) > form > button',{'timeout':3000})
        await page.click('#root > div > main > div > div > div > div > div.signQr-rightContainer > div > div.SignContainer-content > div > div:nth-child(1) > form > button')
        #获取图片
        unget=True
        while unget:
            await self.get_pic_url(page)
            #获得移动距离
            dis=await self.get_distance()
            print(dis)
            #移动滑块
            await self.sliding(page,dis)
            await asyncio.sleep(3)

            #判断是否成功
            cookies = await page.cookies()
            new_url=page.url
            if new_url==home_url:
                unget=False
            else:
                await page.waitForSelector('body > div.yidun_popup--light.yidun_popup.yidun_popup--size-small > div.yidun_modal__wrap > div > div > div.yidun_modal__body > div > div.yidun_panel > div > div.yidun_top > div > button.yidun_refresh',{'timeout': 3000})
                await page.click('body > div.yidun_popup--light.yidun_popup.yidun_popup--size-small > div.yidun_modal__wrap > div > div > div.yidun_modal__body > div > div.yidun_panel > div > div.yidun_top > div > button.yidun_refresh')
        return cookies,page,browser


    # 执行异步
    def get_cookie(self):
        return asyncio.get_event_loop().run_until_complete(self.main(self.name,self.password))

