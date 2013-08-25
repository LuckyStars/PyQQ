# -*- coding: UTF-8 -*-
import urllib
import urllib2
import cookielib
import re
import encrypt
import json, sys, os
import random
import ai
import threading
from Queue import Queue
from nameingroup import self_name

class PyQQ:

    ExploereHEADERS = {
        "Content-type": "application/x-www-form-urlencoded",
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
    
    def GetWeb(self, url, method = 'get', values = ''):
        if method == 'get':
            req = urllib2.Request(url, headers = self.ExploereHEADERS)
        else:
            #print values
            #data = urllib.urlencode({'r': json.dumps(values)})
            #print data
            #ExploereHEADERS['Referer'] = 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3'
            req = urllib2.Request(url, values, headers = self.ExploereHEADERS)
        response = urllib2.urlopen(req)
        the_page = response.read()
        response.close() #不用了就关闭掉
        return the_page;
    
    def __init__(self, qqnum = None, pwd = None):
        if qqnum and pwd:
            self.login(qqnum, pwd)
    
    def login(self, qqnum, pwd):
        if type(qqnum) == type(0):
            qqnum = str(qqnum)
            
        web = self.GetWeb('http://check.ptlogin2.qq.com/check?uin=' + qqnum +'&appid=1003903&r=0.6331230279734363')
        #print web
        state = re.compile("'(.*?)'").findall(web)[0]
        # print cj
        self.uin = qqnum
        self.pwd = pwd
        self.verifycode = re.compile("'(.*?)'").findall(web)[1]
        if state == '1':
            gif = self.GetWeb('http://captcha.qq.com/getimage?aid=1003903&r=0.45623475915069394&uin=' + self.uin)
            file = open(os.getcwd()+'\qq' + qqnum +'code.bmp','w+b')
            file.write(gif)
            file.close()
            self.verifycode = raw_input('[' + qqnum + "] 输入验证码呗:")
        p = encrypt.encrypt(self.pwd, self.uin, self.verifycode)
        loginURL = 'https://ssl.ptlogin2.qq.com/login?u=' + self.uin + \
                    '&p=' + p + \
                    '&verifycode=' + self.verifycode + \
                    '&webqq_type=10&remember_uin=1&login2qq=1&aid=1003903&u1=http%3A%2F%2Fweb.qq.com%2Floginproxy.html%3F' + \
                    'login2qq%3D1%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=2-22-19371&'+ \
                    'mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10017&login_sig=H1HNZ8CjZK5qNcZM1KOzjaHK6jFt5ZLoF*snOAhi9zi2k-NDzZt21r8vgsTwXVrg'
        # print loginURL
        login = self.GetWeb(loginURL)        
        info = re.compile("'(.*?)'").findall(login)
#        print info
        print '用户:[' + info[5] + '(' + self.uin + ')]' + info[4]
        #成功是返回0
        if info[0] != '0':
            print random.choice(['不识字啊喂！','重新来过吧', '弱爆了，这也能看错？'])
            self.login(qqnum, pwd)
        # print cj
        for cookie in self.cj:
            if cookie.name == 'ptwebqq':
                self.ptwebqq = cookie.value
                break 
    
        # print ptwebqq
        self.clientid = '51167527'
        data = 'r=%7B%22status%22%3A%22online%22%2C%22ptwebqq%22%3A%22' + self.ptwebqq + \
               '%22%2C%22passwd_sig%22%3A%22%22%2C%22clientid%22%3A%2251167527%22%2C%22'\
               'psessionid%22%3Anull%7D&clientid=51167527&psessionid=null'
        
        #{"retcode":103,"errmsg":""} {"retcode":121,"t":"0"} {"retcode":100006,"errmsg":""}
        # 返回103、121，代表连接不成功，需要重新登录；
        # 返回102，代表连接正常，此时服务器暂无信息；
        # 返回0，代表服务器有信息传递过来：包括群信、群成员给你的发信，QQ好友给你的发信。
        login2 = self.GetWeb('http://d.web2.qq.com/channel/login2', 'post', data)
        # print login2
        dic = eval(login2)
        # print dic
        
        self.vfwebqq = dic['result']['vfwebqq']
        self.psessionid = dic['result']['psessionid']
        
        getUserFriend = 'http://s.web2.qq.com/api/get_user_friends2'
        hash = encrypt.get_hash(self.uin, self.ptwebqq)
        data = 'r=%7B%22h%22%3A%22hello%22%2C%22hash%22%3A%22' + hash + '%22%2C%22vfwebqq%22%3A%22'\
               + self.vfwebqq + '%22%7D'
        userfriend = self.GetWeb(getUserFriend,'post', data)
        # print userfriend
        
        #fri = json.loads(userfriend.decode(sys.stdin.encoding).encode('utf8'))
        #fri = json.loads(userfriend)
        self.friend = json.loads(userfriend)['result']['info']
        
        # 这个能得到真正的QQ号
        getUserFriend = 'http://web2-b.qq.com/api/get_user_friends'
        data = 'r=%7B%22h%22%3A%22hello%22%2C%22vfwebqq%22%3A%22'\
               + self.vfwebqq + '%22%7D'
        userfriend = self.GetWeb(getUserFriend,'post', data)
        # print userfriend
        qqfriend = json.loads(userfriend)['result']['info']
        
        for user in self.friend:
            for qquser in qqfriend:
                if user['flag'] == qquser['flag']:
                    user['qq'] = qquser['uin']
                    continue
        
        getGroup = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
        data = 'r=%7B%22vfwebqq%22%3A%22' + self.vfwebqq + '%22%7D'
        usergroup = self.GetWeb(getGroup,'post', data)
#        print usergroup
        self.group = json.loads(usergroup)['result']['gnamelist']
#        print self.group
        
        getGroup = 'http://s.web2.qq.com/api/get_friend_uin2?' + \
                   'tuin=%d&verifysession=&type=4&code=&vfwebqq=' + self.vfwebqq + '&t=1375202994632'
        for gp in self.group:
            item = self.GetWeb(getGroup%gp['code'])
            gp[u'gpid'] = int(json.loads(item)['result']['account'])
        
    def getMessage(self):
        data = 'r=%7B%22clientid%22%3A%22' + self.clientid +\
               '%22%2C%22psessionid%22%3A%22' + self.psessionid +\
               '%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid=' + self.clientid +\
               '&psessionid=' + self.psessionid
        #print cj
        rollURL = 'http://d.web2.qq.com/channel/poll2'
        roll = self.GetWeb(rollURL,'post', data)
        try:
            message = json.loads(roll)['result']
        except:
            print 'roll' + roll
        if not message:
            return []
        msgs = []
        for msg in message:
            if msg['poll_type'] == u'message':
                msgs.append({'from':msg['value']['from_uin'], 'data':msg['value']['content'][1].strip(), 'type':msg['poll_type']})
            elif msg['poll_type'] == u'group_message':
#                print msg
                msgdata = msg['value']['content'][1].strip()
                if msgdata.find(self_name)!=-1:                                        
                    msgdata = msgdata.replace(self_name,'').strip()
                    msgs.append({'from':msg['value']['from_uin'], 'data':msgdata, 'type':msg['poll_type']})
        return msgs
    
    def getMessageAll(self):
        data = 'r=%7B%22clientid%22%3A%22' + self.clientid +\
               '%22%2C%22psessionid%22%3A%22' + self.psessionid +\
               '%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid=' + self.clientid +\
               '&psessionid=' + self.psessionid
        #print cj
        rollURL = 'http://d.web2.qq.com/channel/poll2'
        roll = self.GetWeb(rollURL,'post', data)
        try:
            message = json.loads(roll)['result']
        except:
            print 'roll' + roll
        msgs = []
        for msg in message:
            if msg['poll_type'] == u'message' or msg['poll_type'] == u'group_message':
                msgs.append({'from':msg['value']['from_uin'], 'data':msg['value']['content'][1].strip(), 'type':msg['poll_type']})
        return msgs
        
    # webQQ发送时不稳定不可靠的
    # 消息发送不出去的常见原因：
    #1、发送之后直接返回错误页面，说明参数，转码，COOKIES不对！
    #2、返回0，一开始能发送出去，后来却又发送不去了，原因可能是程序采用单线程运作，
    #   这种现象经常会出现，在我们发送消息的时候，需要一个线程去获取消息，即POLL。
    #   简单来说，发送消息和接收消息需要两个独立的线程单独完成，不可将其合成一个线程里面。
    #   再有就是"msg_id":23500002,看看是否累加1，前面的数字是随机数，后面的数字需要累加，
    #   第1条消息就是1，第二条消息就是2。。。
    def sendMessage(self, qqnum, content, method = "uin"):
        #msgID = '41760010'
        if type(qqnum) in (type(u''), type('')):
            qqnum = int(qqnum)

        if method != 'uin': #通过发送到QQ号的方式发送消息
            for users in self.friend:
                if users['qq'] == qqnum:
                    user = users
                    break
        else :
            for users in self.friend:
                if users['uin'] == qqnum:
                    user = users
                    break
        
        if user.get('msgID') == None:
            user['msgID'] = str(random.randint(10000000,99999999));
        else :
            msgID = int(user['msgID'])
            msgID = msgID + 1
            user['msgID'] = str(msgID)
        #msgID = str(random.randint(10000000,99999999))
        data = 'r=%7B%22to%22%3A'+ str(user['uin']) + '%2C%22face%22%3A'+ str(user['face'])+'%2C%22content%22%3A%22%5B%5C%22'\
               + urllib.quote((str(content)).decode(sys.stdin.encoding).encode('utf8')) +\
               '%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%'+\
               '5C%22%3A%5C%22%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%5C%22%2C%5C%22size%5C%22%3A%5C%2211%5C%22%2C%5C%22style%5C%22%'+\
               '3A%5B1%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22800080%5C%22%7D%5D%5D%22%2C%22msg_id%22%3A' + str(user['msgID']) + '%2C%22' + \
               'clientid%22%3A%22' + self.clientid +\
               '%22%2C%22psessionid%22%3A%22' + self.psessionid + \
               '%22%7D&clientid=' + self.clientid +\
               '&psessionid='+ self.psessionid
        sendURL = 'http://d.web2.qq.com/channel/send_buddy_msg2'
        try:
            send = self.GetWeb(sendURL, 'post', data)
        except:
            print '我已经没什么好说的了，砍死咸菜！！！！' 
#        print send
        print "消息[" + content + "]发送完毕"
        
    def sendGroupMessage(self, gid, content, method = "uin"):
        if type(gid) in (type(u''), type('')):
            gid = int(gid)
        user = {}
        if method != 'uin': #通过发送到QQ群号的方式发送消息
            for gps in self.group:
                if gps['gpid'] == gid:
                    user = gps
                    break
        else :
            for gps in self.group:
                if gps['gid'] == gid:
                    user = gps
                    break
        if not user:
            return
#        print user
        if user.get('msgID') == None:
            user['msgID'] = str(random.randint(10000000,99999999));
        else :
            msgID = int(user['msgID'])
            msgID = msgID + 1
            user['msgID'] = str(msgID)
        data = 'r=%7B%22group_uin%22%3A'+ str(user['gid']) + '%2C%22content%22%3A%22%5B%5C%22'\
               + urllib.quote((str(content)).decode(sys.stdin.encoding).encode('utf8')) +\
               '%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%'+\
               '5C%22%3A%5C%22%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%5C%22%2C%5C%22size%5C%22%3A%5C%2211%5C%22%2C%5C%22style%5C%22%'+\
               '3A%5B1%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22800080%5C%22%7D%5D%5D%22%2C%22msg_id%22%3A' + str(user['msgID']) + '%2C%22' + \
               'clientid%22%3A%22' + self.clientid +\
               '%22%2C%22psessionid%22%3A%22' + self.psessionid + \
               '%22%7D&clientid=' + self.clientid +\
               '&psessionid='+ self.psessionid
        sendURL = 'http://d.web2.qq.com/channel/send_qun_msg2'
        try:
            send = self.GetWeb(sendURL, 'post', data)
        except:
            print '我已经没什么好说的了，砍死咸菜！！！！' 
        print "群消息[" + content + "]发送完毕"

class Get(threading.Thread):
    def __init__(self, qq, queue):
        threading.Thread.__init__(self, name=qq)
        self.data = queue  
        self.qq = qq
    def run(self):  
        while True: 
            msg = self.qq.getMessage()
            print msg
            self.data.put(msg)

class Send(threading.Thread):
    def __init__(self, qq, queue): 
        threading.Thread.__init__(self, name=qq) 
        self.data = queue
        self.qq = qq
    def run(self):
        while True:
            msgs = self.data.get()
            print msgs
            for msg in msgs:
                if msg['type'] == u'message':
                    self.qq.sendMessage(msg['from'], ai.magic(msg['data']), "uin")
                elif msg['type'] == u'group_message':
                    self.qq.sendGroupMessage(msg['from'], ai.magic(msg['data']), "uin")
                    
if __name__ == '__main__':
    qq = PyQQ()
    qq.login('111111', '111111')
    friend = qq.friend
#    print friend
    qq.sendGroupMessage(321984505, "你好啊，这是咩啊", "GID")
#    qq.sendMessage(810841055, "你好啊，这是咩啊", "QQ")
#    queue = Queue()
#    get = Get(qq, queue)
#    send = Send(qq, queue)
#    get.start()
#    send.start()
#    while True:
#        try:
#            msgs = qq.getMessage()
#        except:
#            continue
#        print msgs
#        for msg in msgs:
#            qq.sendMessage(msg['from'], ai.magic(msg['data']), "uin")
#    qq.sendMessage(810841055, "你好啊，这是咩啊", "QQ")