# -*- coding: UTF-8 -*-

import requests
import json
import re

base_url = 'https://hsmarket.eastmoney.com/api'


def loads_jsonp(_jsonp):

    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except Exception as e:
        print str(e)
        raise ValueError('five quote request failed...')


def quoteSnapshot(stockCode):
    url = base_url + '/SHSZQuoteSnapshot?callback=jsonp67&id='
    url += stockCode
    # print '*' * 50
    # print 'five quote:'
    # print url
    response = requests.get(url)
    try:
        jsonp = response.content
        # print jsonp
        # print '*' * 50
        j = loads_jsonp(jsonp)
        return j
    except Exception as e:
        print str(e)
