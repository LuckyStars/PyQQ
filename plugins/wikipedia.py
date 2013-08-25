#-*-coding:utf-8-*-

# 维基百科

from pyquery import PyQuery
import requests
import re

def test(data, bot=None):
    return '什么是' in data

def handle(data, bot=None):
    m = re.search('(?<=什么是)(.+?)(?=啊|那|呢|哈|！|。|？|\?|\s|\Z)', data)
    if m and m.groups():
        print m.groups()[0]
        return wikipedia(m.groups()[0])
    raise Exception

def wikipedia(title):
    r = requests.get('http://zh.wikipedia.org/w/index.php', params={'title': title, 'printable': 'yes', 'variant': 'zh-cn'}, timeout=10)
    dom = PyQuery(r.text)
    return dom('#mw-content-text > p:first').remove('sup')[0].text_content()

if __name__ == '__main__':
#    for message in ['什么是SVM  ????', '什么是薛定谔方程啊', '什么是CSS？']:
#        data = message
#        print message, test(data)
#        if test(data):
#            print handle(data)
    print wikipedia('SVM')
