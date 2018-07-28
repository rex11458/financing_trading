# -*- coding: UTF-8 -*-

from market import quoteSnapshot
from user import check_response, current_time


class Trade:
    user = None
    ssrequest = None
    base_url = None

    def __init__(self, user):
        self.user = user
        self.ssrequest = user.ssrequest
        self.base_url = user.base_url

    # 获取资产信息
    def getAssetInfo(self):

        url = self.base_url + '/Assets/GetMyAssests'
        response = self.ssrequest.post(url)
        print('\033[1;31;47m')
        print '*' * 25, '资产信息', current_time(), '*' * 25
        print url
        print 'Asset request data = ', None
        r = check_response(response)
        print 'login response data = ', r
        print '*' * 50
        print('\033[0m')
        return r

    def getCanOperateAmount(self, stockCode, price, tradeType):
        url = self.base_url + '/Trade/GetCanOperateAmount'
        # print '*' * 50
        # print 'get available stock count:'
        # print url
        post_data = {
            'stockCode': stockCode,
            'price': price,
            'tradeType': tradeType
        }
        # print('\033[1;31;47m')
        # print '*' * 25, '可交易股数', current_time(), '*' * 25
        # print url
        # print 'Amount request data = ', post_data
        response = self.ssrequest.post(url, data=post_data)
        r = check_response(response)
        # print 'Amount response data = ', r
        # print '*' * 50
        # print('\033[0m')

        data = r.get('Data')
        try:
            amount = data[0].get('Kczsl')
            return amount
        except Exception as e:
            print '获取可交易股数异常：', str(e)
            # raise ValueError(0)

    def entrust(self, stockCode, tradeType):
        url = self.base_url + '/Trade/SubmitTrade'
        quote = quoteSnapshot(stockCode)
        fivequote = quote.get('fivequote')

        sale_price = fivequote['buy5']
        buy_price = fivequote['sale5']

        if tradeType == 'B':
            price = buy_price
        else:
            price = sale_price
        amount = self.getCanOperateAmount(stockCode, price, tradeType)
        post_data = {
            'stockCode': stockCode,
            'price': price,
            'amount': amount,
            'tradeType': tradeType
        }
        print('\033[1;31;47m')
        print '*' * 25, '委托结果', current_time(), '*' * 25
        print url
        print 'entrust request data = ', post_data
        response = self.ssrequest.post(url, data=post_data)
        r = check_response(response)
        print 'entrust response data = ', r
        print '*' * 50
        print('\033[0m')
        r['amount'] = amount
        r['price'] = price
        return r
