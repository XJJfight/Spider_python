from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json
import re
import csv


'''
1.找到未加密的参数        window.arsea(参数,xxxx)这是加密参数
2.想办法把参数进行加密（必须参考网易的逻辑），params,encSecKey
3.请求到网易，拿到评论信息
'''

url1 = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
#请求方式是post
#真实参数
data = {
    'csrf_token' : "",
    'cursor': "-1",
    'offset': "0",
    'orderType': "1",
    'pageNo': "1",
    'pageSize': "20",
    'rid': "R_SO_4_1325905146",
    'threadId': "R_SO_4_1325905146"
}
#处理加密过程,网页上找到window.asrsea函数是用来加密，又找到一下赋值：window.asrsea=d;window.ecnonasr = e,所以加密函数如下
'''
function a(a) { #返回随机的a位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)  #当a=16，循环16次
            e = Math.random() * b.length,  #随机数
            e = Math.floor(e),  #取整
            c += b.charAt(e);  #取字符串某个位
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {   #采用AES加密，c是密钥，即b是密钥
            iv: d,  #iv:偏移量
            mode: CryptoJS.mode.CBC   #mode模式：cbc
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),  #g是密钥
        h.encText = b(h.encText, i), #返回的就是params，i是密钥
        h.encSecKey = c(i, e, f),  #返回的就是encSecKey，e、f是定死的，只有i会产生偏差，c又不产生随机数，i固定则c也固定
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    
    params跑了两次加密
'''

#window.asrsea输入参数如下：
'''
var bKB0x = window.asrsea(JSON.stringify(i6c), buU9L(["流泪", "强"]), buU9L(Rg1x.md), buU9L(["爱心", "女孩", "惊恐", "大笑"]));
e6c.data = j6d.cr7k({
    params: bKB0x.encText,
    encSecKey: bKB0x.encSecKey
})

则d就是JSON.stringify(i6c)，i6c就是data
    i6c:
        csrf_token: ""
        cursor: "-1"
        offset: "0"
        orderType: "1"
        pageNo: "1"
        pageSize: "20"
        rid: "R_SO_4_1325905146"
        threadId: "R_SO_4_1325905146"

e、f、g是对字符串进行buU9L函数处理
分别跑一下函数，得出
e=buU9L(["流泪", "强"])="010001"
f=buU9L(Rg1x.md)="0CoJUm6Qyw8W8jud"
g=buU9L(["爱心", "女孩", "惊恐", "大笑"])="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"

'''
#d:数据，e：010001，f：00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a8
# 76aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a4
# 6bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
#g:0CoJUm6Qyw8W8jud

e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'hrLCshj8cuy8p0Tw'

def get_encSecKey():
    return '402b9f23777b698212a3d2caa32bb306ddb248a5d080b3a247068f93b75ab3df2eb5fbb260ad05c302be72d6940e93a44ca0c466305fb3d8254670f265b24cfc8ce7a0a70f7d108c592198452019a7fbf6c0d6081c55927e97e38cfdedae2d43bf4ce11ec860fef799210228187ca7bddef861f133f1825a29927ecbd63f2b60'


def get_params(data):
    first = enc_params(data ,g)
    second = enc_params(first , i)
    return second

#加密的内容长度必须为16的倍数
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data

def enc_params(data , key):
    iv = '0102030405060708'
    data = to_16(data)
    aes = AES.new(key = key.encode('utf-8') , IV = iv.encode('utf-8') , mode = AES.MODE_CBC)  #创建加密器
    bs = aes.encrypt(data.encode('utf-8')) #加密
    return str(b64encode(bs) , 'utf-8') #base64编码


#处理完信息后可以开始爬取
resp = requests.post(url = url1 , data = {
    'params' : get_params(json.dumps(data)),
    'encSecKey' : get_encSecKey()
})

page_text = resp.text

iter1 = re.compile(r'.*?"nickname":"(?P<user_name>.*?)".*?'
                   r'"content":"(?P<user_comment>.*?)",.*?'
                   r'"timeStr":"(?P<comment_time>.*?)".*?'
                   r'"likedCount":(?P<comment_like>.*?),"replyCount":(?P<user_reply>.*?),.*?', re.S)

result = iter1.finditer(page_text)

fp1 = open('./wangyi_comment.text' , 'w' , encoding= 'utf-8')

for item in result:

    comment_detail = item.groupdict('')

    comment_detail['user_comment'] = comment_detail['user_comment'].replace('\\n' , ' ')

    print(comment_detail['user_name'] , '\n' , comment_detail['user_comment'] , '\n' ,
          comment_detail['comment_time'] , '\n' , comment_detail['comment_like'] , '\n' ,
          comment_detail['user_reply'])

    fp1.write(comment_detail['user_name'] + '\n' + comment_detail['user_comment'] + '\n' +
              comment_detail['comment_time'] + '\n' + comment_detail['comment_like'] + '\n' +
              comment_detail['user_reply'] + '\n')

print('热门评论信息爬取完毕')

