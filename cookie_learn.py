import requests
import json
'''
f12界面勾选
preserve log 保存日志
disable catch 禁用缓存
才能看登录的信息，拿到登录界面的url

登录，得到cookie
带着cookie，进行后续的浏览爬取
可以用session进行请求，session是一连串的请求，在这个过程中的cookie不会丢失
'''
#登录界面
url1='https://passport.17k.com/ck/user/login'
header1={'User-Aent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
session=requests.session()
data1={
    'loginName': '13326786127',
    'password' : 'Xiejiajian34'
}
session.post(url=url1,data=data1)
#print(resp.text)
#print(resp.cookies) #看cookie
#拿对应数据，刚才的session是有cookie的，用回那个
resp=session.get('https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919')

'''
用requests也可以实现上述功能
resp=requests.get('网址',headers={
    "Cookie":把一大串cookie复制上去
'''

'''
实时更新页面，爬取到的页面代码可能不存在我们想要的数据，而且可能有虚假地址s
这是防盗链
打开XHR选项
'''
def fangdao():
    url1='https://www.pearvideo.com/video_1734046'
    #避免反爬
    header1 = {
        'User-Aent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': url1 #前一个访问地址，知乎用的就是这个方法
    }
    #防盗链：地址上加上信息表明这个网址的前面一个访问网址是什么，如果直接通过url访问这个网址是不行的
    #这时候就需要在requests信息里包含referer才行
    cont_id=url1.split('_')[1]
    video_status=f'https://www.pearvideo.com/videoStatus.jsp?contId={cont_id}&mrd=0.7692048314403361'
    print(video_status)
    response=requests.get(video_status,headers=header1)
    dic=response.json()
    srcUrl=dic['videoInfo']['videos']['srcUrl']
    systemTime=dic['systemTime']
    #关键词替换
    srcUrl=srcUrl.replace(systemTime,f'cont-{cont_id}')
    print(srcUrl)
    #永久性保存
    with open('a.mp4',mode='wb') as f:
        f.write(requests.get(srcUrl).content)

'''
代理原理：通过第三方的一个机器去发送请求,简历代理池，循环使用代理
'''
def daili():
    #自己的代理池
    proxies={
        'https':'https://218.60.8.83:3129',
        'https': 'https://218.61.8.83:3129',
        'https': 'https://218.62.8.83:3129',
    }
    resp=requests.get("https://www.baidu.com",proxies=proxies)
    resp.encoding='utf-8'
    print(resp.text)
    #用代理会使得访问速度下降