#-*-coding:utf-8-*-

# 从simsimi读数据

import sys
sys.path.append('..')

import requests
import random

try:
    from settings import SIMSIMI_KEY
except:
    SIMSIMI_KEY = ''


class SimSimi:

    def __init__(self):

        self.session = requests.Session()

        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        self.api_url = 'http://sandbox.api.simsimi.com/request.p?key=%s&lc=ch&ft=1.0&text=%s'

        if not SIMSIMI_KEY:
            self.initSimSimiCookie()

    def initSimSimiCookie(self):
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:18.0) Gecko/20100101 Firefox/18.0'})
        self.session.get('http://www.simsimi.com/talk.htm')
        self.session.headers.update({'Referer': 'http://www.simsimi.com/talk.htm'})
        self.session.get('http://www.simsimi.com/talk.htm?lc=ch')
        self.session.headers.update({'Referer': 'http://www.simsimi.com/talk.htm?lc=ch'})
        self.session.headers.update({'X-Requested-With': 'XMLHttpRequest'})

    def getSimSimiResult(self, message, method='normal'):
        if method == 'normal':
            r = self.session.get(self.chat_url % message)
        else:
            url = self.api_url % (SIMSIMI_KEY, message)
            r = requests.get(url)
        return r

    def chat(self, message=''):
        if message:
            r = self.getSimSimiResult(message, 'normal' if not SIMSIMI_KEY else 'api')
#            print r.json()
            try:
                answer = r.json()['response']#.encode('utf-8')                
                return answer
            except:
                return random.choice(['呵呵', '。。。', '= =', '=。=', '傻×了吧', '砍死咸菜啊！'])
        else:
            return '叫我干嘛'

simsimi = SimSimi()


def test(data, bot):
    return True


def handle(data, bot):
    return simsimi.chat(data)

if __name__ == '__main__':
    print handle('咸菜', None)