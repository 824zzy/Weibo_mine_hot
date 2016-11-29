# encoding=utf-8
import requests
import json
import re
import base64
import rsa
import binascii


def getLoginInfo():
    preLoginURL = r'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
    html = requests.get(preLoginURL).text
    jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
    data = json.loads(jsonStr)
    servertime = data["servertime"]
    nonce = data["nonce"]
    pubkey = data["pubkey"]
    rsakv = data["rsakv"]
    return servertime, nonce, pubkey, rsakv


def getSu(username):
    """加密用户名，su为POST中的用户名字段"""
    su = [base64.b64encode(username.encode('utf-8')).decode('utf-8')]
    return su




def getSp(password, servertime, nonce, pubkey):

    """加密密码，sp为POST中的用户名字段"""
    pubkey = int(pubkey, 16)
    key = rsa.PublicKey(pubkey, 65537)
    # 以下拼接明文从js加密文件中得到
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    message = message.encode('utf-8')
    sp = rsa.encrypt(message, key)
    # 把二进制数据的每个字节转换成相应的2位十六进制表示形式。
    sp = binascii.b2a_hex(sp)
    return sp

def login():
    servertime, nonce, pubkey, rsakv = getLoginInfo()
    su = getSu("15802252189")
    sp = getSp("kobe81", servertime, nonce, pubkey)
    postData = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        "pagerefer": "http://open.weibo.com/wiki/2/statuses/home_timeline",
        "vsnf": "1",
        "su": su,
        "service": "miniblog",
        "servertime": servertime,
        "nonce": nonce,
        "pwencode": "rsa2",
        "rsakv": rsakv,
        "sp": sp,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "prelt": "126",
        "url": "http://open.weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype": "META",
    }
    loginURL = r'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    session = requests.Session()
    res = session.post(loginURL, data=postData)
    html = res.content.decode('gbk')
    info = re.findall(r"location\.replace\(\'(.*?)\'", html)[0]
    if 'retcode=0' in info:
        print("登录成功！")
    else:
        print("登录失败！")

    return session

# if __name__ == '__main__':


    # session = login()
    # a = session.get("http://s.weibo.com/weibo/lalala&nodup=1&page=2")
    # print a.text
