# -*- coding: UTF-8 -*-

from PyQQ import PyQQ
from PyQQ import Get
from PyQQ import Send
from Queue import Queue
import re
from account import accounts


def getQQ(accounts):
    qqs = []
    for account in accounts:
        qq = PyQQ()
        qq.login(account[0], account[1])
        qqs.append(qq)
    return qqs

if __name__ == '__main__':
    qqs = getQQ(accounts)
    queue = Queue()
    for qq in qqs:
        get = Get(qq, queue)
        send = Send(qq, queue)
        get.start()
        send.start()
    
    
    