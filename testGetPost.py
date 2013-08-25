# -*- coding: UTF-8 -*-
import urllib
import urllib2
import cookielib
import re
import encrypt
import json, sys, os
import random

##reload(sys)
##sys.setdefaultencoding('utf8')


from urllib2 import URLError

ExploereHEADERS = {"Content-type": "application/x-www-form-urlencoded",
           'Accept-Language':'zh-CN,zh;q=0.8',
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0;Windows NT 5.0)',
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Connection": "close",
           "Cache-Control": "no-cache",
            "Referer": "http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3"
            }

#设置cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# 安装cookie
urllib2.install_opener(opener)

def GetWeb(url,values,method ='get'):
    if method == 'get':
        req = urllib2.Request(url, headers = ExploereHEADERS)
    else:
        #print values
        #data = urllib.urlencode({'r': json.dumps(values)})
        #print data
        #ExploereHEADERS['Referer'] = 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3'
        req = urllib2.Request(url, values, headers = ExploereHEADERS)
    response = urllib2.urlopen(req)
    the_page = response.read()
    response.close() #不用了就关闭掉
    return the_page;

web =  GetWeb('http://check.ptlogin2.qq.com/check?uin=1213247447&appid=1003903&r=0.6331230279734363','')
print web
state = re.compile("'(.*?)'").findall(web)[0]
# print cj
password = 'wr6740495'
uin = '1213247447'
verifycode = re.compile("'(.*?)'").findall(web)[1]
if state == '1':
    gif = GetWeb('http://captcha.qq.com/getimage?aid=1003903&r=0.45623475915069394&uin=' + uin, '')
    file = open(os.getcwd()+'\qqcode.bmp','w+b')
    file.write(gif)
    file.close()
    verifycode = raw_input("输入验证码呗:")
p = encrypt.encrypt(password, uin, verifycode)


loginURL = 'https://ssl.ptlogin2.qq.com/login?u='+uin+'&p='+p+'&verifycode='+verifycode+'&webqq_type=10&remember_uin=1&login2qq=1&aid=1003903&u1=http%3A%2F%2Fweb.qq.com%2Floginproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=2-22-19371&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10017&login_sig=H1HNZ8CjZK5qNcZM1KOzjaHK6jFt5ZLoF*snOAhi9zi2k-NDzZt21r8vgsTwXVrg'

# print loginURL

login = GetWeb(loginURL,'')
print login
# print cj
for cookie in cj:
    print(cookie.name, cookie.value)
    if cookie.name == 'ptwebqq':
        ptwebqq = cookie.value

# print ptwebqq
clientid = '51167527'
data = 'r=%7B%22status%22%3A%22online%22%2C%22ptwebqq%22%3A%22'\
       +ptwebqq+\
       '%22%2C%22passwd_sig%22%3A%22%22%2C%22clientid%22%3A%2251167527%22%2C%22'\
       'psessionid%22%3Anull%7D&clientid=51167527&psessionid=null'

#{"retcode":103,"errmsg":""} {"retcode":121,"t":"0"} {"retcode":100006,"errmsg":""}
# 返回103、121，代表连接不成功，需要重新登录；
# 返回102，代表连接正常，此时服务器暂无信息；
# 返回0，代表服务器有信息传递过来：包括群信、群成员给你的发信，QQ好友给你的发信。
login2 = GetWeb('http://d.web2.qq.com/channel/login2', data,'post')
print login2
dic = eval(login2)

vfwebqq = dic['result']['vfwebqq']
psessionid = dic['result']['psessionid']

#r    {"h":"hello","hash":"F8F6ACAC","vfwebqq":"9a8d442b02dbde99248a85eb59aababc5f48785c48b74ca70be3962d3a5537ebdc330f66595221a2"}
#r=%7B%22h%22%3A%22hello%22%2C%22hash%22%3A%22F8F6ACAC%22%2C%22vfwebqq
#%22%3A%229a8d442b02dbde99248a85eb59aababc5f48785c48b74ca70be3962d3a5537ebdc330f66595221a2%22%7D
getuserfriend = 'http://s.web2.qq.com/api/get_user_friends2'
data = 'r=%7B%22h%22%3A%22hello%22%2C%22vfwebqq%22%3A%22'\
       + vfwebqq + '%22%7D'
userfriend = GetWeb(getuserfriend,data,'post')
print "user friends"
print data
print userfriend

data = 'r=%7B%22clientid%22%3A%22' + clientid +\
       '%22%2C%22psessionid%22%3A%22' + psessionid +\
       '%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid=' + clientid +\
       '&psessionid=' + psessionid
#print cj
#收信息
rollURL = 'http://d.web2.qq.com/channel/poll2'
roll = GetWeb(rollURL,data,'post')
print roll

#fri = json.loads(userfriend.decode(sys.stdin.encoding).encode('utf8'))
fri = json.loads(userfriend)
print fri
me = fri['result']['info'][0]
print me

#msgID = '41760010'
msgID = str(random.randint(10000000,99999999))
data = 'r=%7B%22to%22%3A'+ str(me['uin']) + '%2C%22face%22%3A'+ str(me['face'])+'%2C%22content%22%3A%22%5B%5C%22'\
       + urllib.quote(('能不能收到'+msgID).decode(sys.stdin.encoding).encode('utf8')) +\
       '%5C%22%2C%5C%22%5C%5Cn%E3%80%90%E6%8F%90%E7%A4%BA%EF%BC%9A%E6%AD%A4%E7%94%A8%E6%88%B7%E6%AD%A3%E5%9C%A8%E4%BD'+\
       '%BF%E7%94%A8Q%2B%20Web%EF%BC%9Ahttp%3A%2F%2Fweb.qq.com%2F%E3%80%91%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%'+\
       '5C%22%3A%5C%22%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%5C%22%2C%5C%22size%5C%22%3A%5C%2211%5C%22%2C%5C%22style%5C%22%'+\
       '3A%5B1%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22800080%5C%22%7D%5D%5D%22%2C%22msg_id%22%3A' + msgID + '%2C%22' + \
       'clientid%22%3A%22' + clientid +\
       '%22%2C%22psessionid%22%3A%22' + psessionid + \
       '%22%7D&clientid=' + clientid +\
       '&psessionid='+ psessionid
print msgID
sendURL = 'http://d.web2.qq.com/channel/send_buddy_msg2'
send = GetWeb(sendURL, data, 'post')
print send
print "发送完毕"

# 这个能得到真正的QQ号
getuserfriend = 'http://web2-b.qq.com/api/get_user_friends'
data = 'r=%7B%22h%22%3A%22hello%22%2C%22vfwebqq%22%3A%22'\
       + vfwebqq + '%22%7D'
userfriend = GetWeb(getuserfriend,data,'post')
print userfriend
