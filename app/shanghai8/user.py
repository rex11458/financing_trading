# -*- coding: UTF-8 -*-

import requests
import hashlib
from datetime import datetime

base_url = 'http://m.shangshang8.com/Ashx'


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_response(response):
    try:
        j = response.json()
        return j
    except Exception as e:
        print str(e)


class User:
    _userId = None
    _password = None

    ssrequest = requests.Session()

    def setUserId(self, userId):
        self._userId = userId

    def setPassword(self, password):
        self._password = password

    # 登录
    def login(self):
        url = base_url + '/AccountHandler.ashx'
        original = self._password
        hl = hashlib.md5()
        hl.update(original)
        password = hl.hexdigest()
        data = {
            'Method': 'Login',
            'username': self._userId,
            'password': password,
        }
        print('\033[1;31m')
        print '*' * 25, '登录信息', current_time(), '*' * 25
        print url
        print 'login request data = ', data
        response = self.ssrequest.get(url, data=data)
        r = check_response(response)
        print 'login response data = ', r
        print '*' * 50
        print('\033[0m')
        return r
