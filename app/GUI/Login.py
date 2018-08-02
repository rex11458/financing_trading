# -*- coding: UTF-8 -*-

import wx
import requests
import random
from io import BytesIO

class LoginFrame(wx.Frame):
    acc = None
    pwd = None
    vcode = None
    bmp = None
    confirm = None
    def __init__(self, *args, **kw):
        super(LoginFrame, self).__init__(*args, **kw)

        pnl = wx.Panel(self)
        self.acc = wx.TextCtrl(pnl,value='13818353412', style=wx.TE_LEFT,size=(200, 25), pos=(200, 60))
        self.pwd = wx.TextCtrl(pnl,value='lxh123456', style=wx.TE_PASSWORD,size=(200, 25), pos=(200, 100))
        # self.vcode = wx.TextCtrl(pnl, style=wx.TE_LEFT,size=(60, 25), pos=(200, 138))
        # self.bmp = wx.BitmapButton(pnl, -1, pos=(270, 135),style=0)
        self.confirm = wx.Button(pnl, label='登录', size=(150,30), pos=(250, 180))

    def setVcode(self, vcode):
        image = wx.Image(BytesIO(vcode), wx.BITMAP_TYPE_JPEG)
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        self.bmp.SetBitmap(temp)
        self.bmp.SetSize(size)
   
    def getAcc(self):
        return self.acc.GetValue()

    def getPwd(self):
        return self.pwd.GetValue()

    def getVcode(self):
        return self.vcode.GetValue()

    def getConfirm(self):
        return self.confirm
