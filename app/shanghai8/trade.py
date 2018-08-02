# -*- coding: UTF-8 -*-

from user import check_response, current_time, base_url
from eastmoney.market import quoteSnapshot
import random
import math

globa_hold = {}


class Trade:
    user = None
    ssrequest = None

    def __init__(self, user):
        self.user = user
        self.ssrequest = user.ssrequest

    # 获取持仓信息
    def getHoldInfo(self):
        global globa_hold
        url = base_url + '/TradeHandler.ashx'

        data = {
            'Method': 'GetStockPosition',
        }
        response = self.ssrequest.get(url, data=data)

        print('\033[1;31m')

        print '*' * 25, '持仓信息', current_time(), '*' * 25
        print 'url:', url
        r = check_response(response)
        globa_hold = r
        print r
        print '*' * 50
        print('\033[0m')
        return r

    def buy(self, stockCode):
        url = base_url + '/TradeHandler.ashx'
        quote = quoteSnapshot(stockCode)

        # 股票代码
        ticker = stockCode
        # 当前价格
        realtimequote = quote.get('realtimequote')
        restingPrice = realtimequote.get('currentPrice')
        # 委托价格
        buyPrice = round(float(restingPrice) * 1.02, 2)
        # 配置总额
        pv = 20000
        # 杠杆倍数
        v = 10
        # 保证金
        pb = pv / v
        # 止盈额
        sp = 0
        # 止损额
        sl = int(pv * 0.02 - pb)
        # 买入数量
        buyQuantity = int(math.floor(pv / buyPrice / 100) * 100)

        initQuantity = buyQuantity
        initPrice = buyPrice
        # 随机数
        t = random.random()
        # 委托方式 1：市价委托
        category = 1

        # Method:SubmitBuy
        # ticker:000001
        # pv:100000
        # pb:10000
        # sp:0
        # sl:-8000
        # buyQuantity:10500
        # buyPrice:9.44
        # restingPrice:9.25
        # category:1
        # initQuantity:10500
        # initPrice:9.44
        # t:0.4509517725582237
        data = {
            'Method': 'SubmitBuy',
            'ticker': ticker,
            'pv': pv,
            'pb': pb,
            'sp': sp,
            'sl': sl,
            'buyQuantity': buyQuantity,
            'buyPrice': buyPrice,
            'restingPrice': restingPrice,
            'category': category,
            'initQuantity': initQuantity,
            'initPrice': initPrice,
            't': t
        }
        response = self.ssrequest.post(url, data=data)
        print('\033[1;31m')
        print '*' * 25, '委托结果', current_time(), '*' * 25
        print 'request data = ', data
        response = self.ssrequest.get(url, data=data)

        r = check_response(response)
        print 'entrust response data = ', r
        print '*' * 50
        print('\033[0m')
        return r

    def sell(self, stockCode):

        rows = globa_hold.get('rows')
        if len(rows) == 0:
            return {'code': -1, 'msg': 'no avaliable stocks'}

        for hold in rows:
            contractId = hold.get('contractId')
            ticker = hold.get('ticker')
            if stockCode == ticker:
                contractId = hold.get('contractId')
                r = self.single_sell(contractId)
                return r
        return {'code': -1, 'msg': 'no avaliable stocks'}

    def single_sell(self, contractId):
        url = base_url + '/TradeHandler.ashx'

        data = {
            'Method': 'SubmitSell',
            'category': 1,
            'restingPrice': 0,
            'contractId': contractId
        }
        response = self.ssrequest.post(url, data=data)
        print('\033[1;31m')
        print '*' * 25, '委托结果', current_time(), '*' * 25
        print 'request data = ', data
        response = self.ssrequest.get(url, data=data)
        r = check_response(response)
        print 'entrust response data = ', r
        print '*' * 50
        print('\033[0m')
        return r

    # def getCanOperateAmount(self, stockCode, price, tradeType):
    #     url = self.base_url + '/Trade/GetCanOperateAmount'
    #     # print '*' * 50
    #     # print 'get available stock count:'
    #     # print url
    #     post_data = {
    #         'stockCode': stockCode,
    #         'price': price,
    #         'tradeType': tradeType
    #     }
    #     # print('\033[1;31;47m')
    #     # print '*' * 25, '可交易股数', current_time(), '*' * 25
    #     # print url
    #     # print 'Amount request data = ', post_data
    #     response = self.ssrequest.post(url, data=post_data)
    #     r = check_response(response)
    #     # print 'Amount response data = ', r
    #     # print '*' * 50
    #     # print('\033[0m')

    #     data = r.get('Data')
    #     try:
    #         amount = data[0].get('Kczsl')
    #         return amount
    #     except Exception as e:
    #         print '获取可交易股数异常：', str(e)
    #         # raise ValueError(0)

    def entrust(self, stockCode, tradeType):
        # url = self.base_url + '/Trade/SubmitTrade'
        # quote = quoteSnapshot(stockCode)
        # fivequote = quote.get('fivequote')

        # sale_price = fivequote['buy5']
        # buy_price = fivequote['sale5']

        # if tradeType == 'B':
        #     price = buy_price
        # else:
        #     price = sale_price
        # amount = self.getCanOperateAmount(stockCode, price, tradeType)
        # post_data = {
        #     'stockCode': stockCode,
        #     'price': price,
        #     'amount': amount,
        #     'tradeType': tradeType
        # }
        # print('\033[1;31;47m')
        # print '*' * 25, '委托结果', current_time(), '*' * 25
        # print url
        # print 'entrust request data = ', post_data
        # response = self.ssrequest.post(url, data=post_data)
        # r = check_response(response)
        # print 'entrust response data = ', r
        # print '*' * 50
        # print('\033[0m')
        # r['amount'] = amount
        # r['price'] = price
        return r
