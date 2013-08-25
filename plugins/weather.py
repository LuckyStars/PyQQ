#!/usr/bin/env python
#-*-coding:utf-8-*-


# 天气
import os
import requests
import cPickle as pickle


def city(data):
    cityidDict = pickle.load(file(os.path.join(os.path.dirname(__file__), 'data' + os.path.sep + 'cityid'), 'r'))
    for city in cityidDict:
        if city.encode('utf8') in data:
            return True
    return False


def test(data, bot):
    return '天气' in data and city(data)


def weather(cityid):
    try:
        weatherinfo = requests.get('http://www.weather.com.cn/data/cityinfo/' + cityid + '.html').json()['weatherinfo']
        return (weatherinfo['city'] + ', ' + weatherinfo['weather'] + ', ' + weatherinfo['temp1'] + ' ~ ' + weatherinfo['temp2']).encode('utf8')
    except:
        return 0


def handle(data, bot):
    cityidDict = pickle.load(file(os.path.join(os.path.dirname(__file__), 'data' + os.path.sep + 'cityid'), 'r'))
    for city in cityidDict:
        if city.encode('utf8') in data:
            reply = weather(cityidDict[city])
            return reply if reply else '不会自己去看天气预报啊'


if __name__ == '__main__':
    print test({'message': '天气怎么样'}, None)
    print test({'message': '北京天气怎么样'}, None)
    print handle({'message': '北京天气怎么样', 'author_id': 'HQM'}, None)
