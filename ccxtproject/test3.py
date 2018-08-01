#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 客户端调用，用于查看API返回结
import time
import math
import sys
import ccxt
import pprint

bitz = ccxt.bitz()
apikey = bitz.apiKey = 'e08edbaef8fca9984a652e00386ec2e8'
secretkey = bitz.secret = 'HmctG3DcZyRONEA3d10wyPQ7LvYQbLToE1GFEh92MdvkvfHJaVk5DKgQYVgXoVe6'
bitz.password = 'vJ1cE1fB3rB7fF2'

symbol = 'BZ/USDT'

ticker = bitz.fetch_ticker(symbol)
tickerInfo = ticker['info']



print(ticker)

# initCounter = Info['initCounter']
# baseInfo = Info['baseInfo']
# Names = [info['currency'] for info in baseInfo]
# marketLength = len(baseInfo)
# Balances = [0.0 for i in range(marketLength)]
# buyOrders = [[] for i in range(marketLength)]
# sellOrders = [[] for i in range(marketLength)]
#
# #现货API
# okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
#
# flagShow = True
# def checkMyOrders(index,orders,targetOrders,Type):
#     temp = [order for order in targetOrders]
#     uselessOrdersID = []
#     for order in orders:
#         seq = order[0]
#         myPrice = order[1]
#         myIOUAmount = order[2]
#         flagUserless = True
#         for target in temp:
#             price = target[0]
#             amount = target[1]
#             if (abs(myPrice/price - 1) < 0.0001) and (abs(myIOUAmount/amount - 1) < 0.1):
#                 temp.remove(target)
#                 flagUserless = False
#                 break
#             if flagUserless:
#                 print('现货取消订单')
#                 print(okcoinSpot.cancelOrder[Names[index]+'_'+Names[0],str(seq)])
#
#     for target in temp:
#         price = target[0]
#         amount = target[1]
#         print(Names[index]+'_'+Names[0],Type,str(price),str(amount))
#
#
# while True:
#     time.sleep(5)
#     try:
#         res = json.loads(okcoinSpot.userinfo())
#
#     except Exception as e:
#             print (e)
#             continue
#     funds = res['info']['funds']
#
#     for i in range(marketLength):
#         Balances[i] = float(funds['free'][Names[i]])+float(funds['freezed'][Names[i]])
#
#     flagsuc = True
#
#     for i in range(1,marketLength):
#         buyOrders[i] = []
#         sellOrders[i] = []
#         try:
#             res = json.loads(okcoinSpot.orderinfo(Names[i]+'_'+Names[0]))
