# coding=utf-8
import binascii
import rsa
import base64
import requests
import re
import json
def prelogin():
    url="https://login.sina.com.cn/sso/prelogin.php?entry=account&callback=sinaSSOController.preloginCallBack&su=MTU2MjAxNTE0NzU%3D&rsakt=mod&client=ssologin.js(v1.4.15)&_=1476186181803"
    html=requests.get(url).text

    jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
    data = json.loads(jsonStr)
    servertime = data["servertime"]
    nonce = data["nonce"]
    pubkey = data["pubkey"]
    rsakv = data["rsakv"]
    return servertime, nonce, pubkey, rsakv

def getSu(username):

    su = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    return su

def getSp(password, servertime, nonce, pubkey):

    pubkey = int(pubkey, 16)
    key = rsa.PublicKey(pubkey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    message = message.encode('utf-8')
    sp = rsa.encrypt(message, key)
    sp = binascii.b2a_hex(sp)
    return sp

def main():
    servertime, nonce, pubkey, rsakv = prelogin()
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
    lst= res.cookies.items()
    cookie=''
    for each in lst:
        cookie+= each[0]+'='+each[1]+';'

    with open('cookies','w') as f:
        f.write(cookie)
    print 'cookies have refreshed'