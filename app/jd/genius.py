# -*- coding: UTF-8 -*-

import os
import urllib2
import json
import hashlib
import time
from datetime import datetime


g_stock_md5 = ''


def fetch_data(url):
    try:
        res_data = urllib2.urlopen(url)
        res = res_data.read()
        return res
    except Exception as e:
        process_exception(e)


def process_exception(e):
    title = '牛人交易信息获取异常'
    content = str(e)
    send_notification(title, content)


def encryption_data(original):
    hl = hashlib.md5()
    hl.update(original)
    return hl.hexdigest()


def send_notification(title, content):
    noti = "osascript -e" + "\'display notification" + " \" " + content
    noti += "\" with title" + "\"" + title + "\" " + " \'"
    os.system(noti)


def process_stock_data(data):
    try:
        j = json.loads(data)
        data = j["data"][0]
        stock = data["convertStocks"][0]
        # 股票名称和代码
        stockName = stock["stockName"]
        stockCode = stock["stockCode"]
        # 卖出份额
        proportionFrom = stock["proportionFrom"]
        # 买入份额
        proportionTo = stock["proportionTo"]
        tradeType = 'B'
        buying = '买入'
        volume = round(proportionTo * 100, 2)
        if proportionFrom > proportionTo:
            buying = '卖出'
            tradeType = 'S'
        # 成交时间
        tradeTime = data["tradeTime"] / 1000
        localTime = time.localtime(tradeTime)
        u_time = time.strftime('%Y-%m-%d %H:%M:%S', localTime)
        # 成交价格
        u_price = str(stock["price"])
        # 成交份额
        u_volume = str(volume)
        content = '成交时间:' + u_time + '\n成交价格：' + u_price
        content += '份额占比:' + u_volume
        title = buying + " " + stockName.encode('utf-8') + ' ' + str(stockCode)

        return {
            'title': title,
            'content': content,
            'time': u_time,
            'tradeType': tradeType,
            'stockCode': stockCode
        }
    except Exception as e:
        process_exception(e)


def fetch_genius_data():
    try:
        global g_stock_md5
        url = "https://gps.jd.com/convert/history?appVersion=2.1.2&appname=jingdonggupiao&channel=AppStore&deviceId=F2E40E18-3E09-4CBE-A9AD-56201F718B40&deviceModel=iPhone&deviceToken=8852fa64f03d3913fd0553a9f93e0786f5709c1da96071045bce1a6bcb3dd0ef&gpsp=semYT/VGwwSDKTJVuyUjHQ%3D%3D&id=12195&idfa=F2E40E18-3E09-4CBE-A9AD-56201F718B40&jailBroken=false&lan=zh-Hans-CN&machineName=iPhone8%2C1&mm=76bd480eb1ba9ee50bb660b3eb1e9f03&p=1&partner=AppStore&platCode=3&platVersion=12.0&ps=10&screen=750%2A1334&timestamp=1528852513&wsKey=AAFa8n1GAED8mXx3vrE16ywyDpJ77z1PQ-n94eGf8DaaAEDG9MZIXf6QcG2xa9OovpG7Aa-QorpxtN-tdzaRDM-FtnxtSQbu"
        data = fetch_data(url)
        processed = process_stock_data(data)
        time = processed['time']
        # title = processed['title']
        # content = processed['content']
        md5_string = encryption_data(time)
        # print('*' * 50)
        print datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print 'global：' + g_stock_md5
        # print '加密前：' + time
        # print '加密后：' + md5_string
        # print(title + content)
        # print('*' * 50)
        if md5_string == g_stock_md5:
            return None
        else:
            if g_stock_md5 == '':
                g_stock_md5 = md5_string
                return
            g_stock_md5 = md5_string
            # print('\033[1;34;47m')
            # print('*' * 50)
            # print(title + content)
            # print('*' * 50)
            # print('\033[0m')
            tradeType = processed['tradeType']
            stockCode = processed['stockCode']
            # send_notification(title, content)
            return {
                'stockCode': stockCode[2:],
                'tradeType': tradeType
            }
            
    except Exception as e:
        process_exception(e)
