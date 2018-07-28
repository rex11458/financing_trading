# -*- coding: UTF-8 -*-

import requests
import random
from datetime import datetime


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
    _identifyCode = None
    _randNumber = None
    base_url = 'https://tradeh5.eastmoney.com'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    ssrequest = requests.Session()
    ssrequest.headers.update(headers)

    def setUserId(self, userId):
        self._userId = userId

    def setPassword(self, password):
        self._password = password

    def setIdentifyCode(self, identifyCode):
        self

    # 是否在线
    def isOnLine(self):
        url = self.base_url + '/More/IsOnline'
        response = self.ssrequest.post(url)
        r = check_response(response)
        return r['Status'] == 1

    # 是否需要验证码
    def isNeedValidCode(self):
        url = self.base_url + '/LogIn/IsNeedValidCode'
        response = self.ssrequest.post(url)
        r = check_response(response)
        return r == 1

    # 获取验证码
    def getValidCode(self):
        rand = random.random()
        self._randNumber = rand
        url = self.base_url + '/LogIn/YZM'
        response = self.ssrequest.get(url, params={'randNum': rand})
        return response.content

    # 登录
    def login(self):
        
        url = self.base_url + '/Login/Authentication'

        data = {
            'userId': self._userId,
            'password': self._password,
            'holdOnlineIdx': 4,
            'type': 'Z',
            'randNumber': self._randNumber,
            'identifyCode': self._identifyCode
            }
        print('\033[1;31;47m')
        print '*' * 25, '登录信息', current_time(), '*' * 25
        print url
        print 'login request data = ', data
        response = self.ssrequest.post(url, data=data)
        r = check_response(response)
        print 'login response data = ', r
        print '*' * 50
        print('\033[0m')
        return r
        