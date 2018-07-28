# -*- coding: UTF-8 -*-

import os
import wx

from shanghai8 import User, Trade
from GUI import LoginFrame
from common import current_time, WorkerThread
from jd import fetch_genius_data


def send_notification(title, content):
    noti = "osascript -e" + "\'display notification" + " \" " + content
    noti += "\" with title" + "\"" + title + "\" " + " \'"
    os.system(noti)


class MainApp(wx.App):
    """Class Main App."""

    def OnInit(self):
        """Init Main App."""
        self.frame = LoginFrame(None, title='User Login', size=(600, 300))
        self.user = User()
        self.trade = Trade(self.user)
        # self.user.isNeedValidCode()
        self.frame.Bind(wx.EVT_BUTTON, self.onLogin, self.frame.confirm)
        # self.frame.Bind(wx.EVT_BUTTON, self.getVcode, self.frame.bmp)
        # self.getVcode(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        return True

    def onLogin(self, event):
        user = self.user
        frame = self.frame
        acc = frame.getAcc()
        pwd = frame.getPwd()

        user._userId = acc
        user._password = pwd

        r = user.login()
        status = r.get('code') == 1
        message = r.get('msg')
        content = ''
        if status is True:
            title = '登录成功'
            self.frame.Close()
            send_notification(title, content)
            self.start()
        else:
            title = '登录失败'
            if message is not None:
                content = message.encode('utf-8')
            send_notification(title, content)

    def start(self):

        thread = WorkerThread(0.1, self.getGeniusTransationData)
        thread.start()

        thread2 = WorkerThread(10 * 60, self.getAssetInfo)
        thread2.start()

    def getAssetInfo(self):
        trade = self.trade
        asset = trade.getHoldInfo()
        title = '持仓信息'
        content = ''
        try:
            total = asset.get('total')
            rows = asset.get('rows')
            title = str(total) + '条持仓信息'

            if len(rows) == 0:
                content = '暂无持仓'
            else:
                lastest = rows[0]
            stockName = lastest.get('stockName')
            deferLv = lastest.get('deferLv')
            content = '股票名称：' + stockName.encode('utf-8') + '\n'
            content += '递延条件：' + deferLv.encode('utf-8')

        except Exception as e:
            content = '获取资产信息失败：' + str(e)
        send_notification(title, content)

    def getGeniusTransationData(self):
        data = fetch_genius_data()
        if data is not None:
            stockCode = data.get('stockCode')
            tradeType = data.get('tradeType')

            content = ''
            if tradeType == 'B':
                r = self.trade.buy(stockCode)
                type = '买入'
            else:
                r = self.trade.sell(stockCode)
                type = '卖出'

            code = r.get('code')
            msg = r.get('msg')
            if code == 1:
                title = type + ' 委托成功 ' + current_time()

            else:
                title = type + ' 委托失败 ' + current_time()
                
            content += '委托代码：' + str(stockCode) + '\n'
            content += msg.encode('utf-8')
            send_notification(title, content)


def start():
    app = MainApp(redirect=False)
    app.MainLoop()


if __name__ == '__main__':
    app = MainApp(redirect=False)
    app.MainLoop()
