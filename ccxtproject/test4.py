#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
import numpy as np
import pandas as pd
import talib
import datetime
import time
import json
import math
import sys

#初始化apikey，secretkey,url
config = open('.config','r')
lines = config.readlines()
apikey = lines[0].strip()
secretkey = lines[1].strip()
config.close()
#请求注意：国内账号需要 修改为 www.okcoin.cn
okcoinRESTURL = 'www.bitz.com'
# okexRESTURL = 'www.okex.com'

#现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

#期货API
okcoinFuture = OKCoinFuture(okexRESTURL,apikey,secretkey)

#海龟参数
total_usd = 4000
lever = 20
#头寸
position = 10
#季度
contract_type = 'quarter'
kline_type  = '1min'
N1=350
nbdev=2.5
# N1=55
# nbdev=2
stop_N = 2
entry_price = 0
last_entry_price = 0
entry_atr = 0
units = 0

while True:
    time.sleep(1)
    try:
        print(u'------')
        print(u'当季期货行情信息')
        trades = okcoinFuture.future_trades('btc_usd',contract_type)
        klines = okcoinFuture.kline('btc_usd',kline_type,contract_type,1001)
        future_userinfo_4fix = okcoinFuture.future_userinfo_4fix()
        future_position_4fix = okcoinFuture.future_position_4fix('btc_usd',contract_type,1)
        future_order_info = okcoinFuture.future_orderinfo('btc_usd',contract_type,'-1','2',1,45)
        future_ticker = okcoinFuture.future_ticker('btc_usd',contract_type)
        if future_userinfo_4fix == '':
            continue
        if future_position_4fix == '':
            continue
        if future_order_info == '':
            continue
        future_userinfo_4fix_json = json.loads(future_userinfo_4fix)
        future_position_4fix_json = json.loads(future_position_4fix)
        future_order_info_json = json.loads(future_order_info)
        holding = future_position_4fix_json['holding']
        orders = future_order_info_json['orders']
        rights = future_userinfo_4fix_json['info']['btc']['rights']
        print(future_userinfo_4fix_json['info']['btc'])
        inputs = {
            'times': np.array([klines[i][0] for i in range(len(klines)-1)]),
            'open': np.array([float(klines[i][1]) for i in range(len(klines)-1)]),
            'high': np.array([float(klines[i][2]) for i in range(len(klines)-1)]),
            'low': np.array([float(klines[i][3]) for i in range(len(klines)-1)]),
            'close': np.array([float(klines[i][4]) for i in range(len(klines)-1)]),
            'volume': np.array([float(klines[i][5]) for i in range(len(klines)-1)])
        }
        ATR = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)
        LAST_ATR = ATR[len(ATR)-1]
        # 海龟法则(布林通道交易)
        # 如果前一日的收盘价穿越了通道的顶部，则在开盘时做多；如果前一日的收盘价跌破通道的底部，则在开盘时做空
        # 止损设置为2N
        # 退出设置为价格反向穿越中轴时
        # 获取入场信号
        curry_price = trades[len(trades)-1]['price']
        # print(curry_price * rights)
        # position = (lever * 0.01 * curry_price * rights) / (100 * LAST_ATR)
        print(u'--头寸规模--')
        print(position)
        # print(math.ceil((lever * 0.01 * curry_price * rights) / (100 * LAST_ATR)))
        print(u'------')
        upperband, middleband, lowerband = talib.BBANDS(inputs['close'], timeperiod=N1, nbdevup=nbdev, nbdevdn=nbdev, matype=0)
        IN_HIGH=upperband[len(upperband)-1]
        IN_LOW=lowerband[len(lowerband)-1]
        OUT_PRICE=middleband[len(lowerband)-1]
        print(u'LAST_ATR:')
        print(LAST_ATR)
        print(u'当前价格:')
        print(curry_price)
        print(u'布林通道上轨价格:')
        print(IN_HIGH)
        print(u'布林通道中轨价格:')
        print(OUT_PRICE)
        print(u'布林通道下轨轨价格:')
        print(IN_LOW)
        # 持仓
        if len(holding) > 0:
            holdingItem = holding[0]
            buy_amount = holdingItem['buy_amount']
            sell_amount = holdingItem['sell_amount']
            #多头
            if buy_amount > 0:
                order = orders[0]
                buy_price_avg = order['price']
                buy_available = holdingItem['buy_available']
                units = buy_available/position
                NEXT_PRICE = round((buy_price_avg + LAST_ATR * 0.5))
                print(u'多头出场平多价格:')
                print(OUT_PRICE)
                # print(units)
                #止损价格
                if curry_price < OUT_PRICE:
                    print(u'当前价格低于止损价格,止损多头.')
                    print(okcoinFuture.future_trade('btc_usd',contract_type,curry_price,buy_available,'3','1','20'))
                    entry_atr = 0
                    pass
                elif units < 4 :
                    print(u'多头下次加码价格:')
                    print(NEXT_PRICE)
                    if curry_price > NEXT_PRICE:
                        print(okcoinFuture.future_trade('btc_usd',contract_type,curry_price,position,'1','1','20'))
                        pass
                    pass
            # 空头
        #     if sell_amount > 0:
        #         order = orders[0]
        #         sell_price_avg = order['price']
        #         sell_available = holdingItem['sell_available']
        #         units = sell_price_avg/position
        #         NEXT_PRICE = round((sell_price_avg - LAST_ATR * 0.5))
        #         # print(units)
        #         #止损价格
        #         if curry_price > OUT_PRICE:
        #             print(u'当前价格低于止损价格,止损空头.')
        #             print(okcoinFuture.future_trade('btc_usd',contract_type,curry_price,sell_available,'4','1','20'))
        #             entry_atr = 0
        #             pass
        #         elif units < 4:
        #             print(u'空头下次加码价格:')
        #             print(NEXT_PRICE)
        #             if curry_price < NEXT_PRICE:
        #                 print(okcoinFuture.future_trade('btc_usd',contract_type,curry_price,position,'2','1','20'))
        #                 pass
        #             pass
        #         pass
        #     #空头
        #     continue
        # #空仓检测进场信号
        # else:
        #     if curry_price > IN_HIGH:
        #         print(u'当前价格高于进场价格,买多')
        #         print(okcoinFuture.future_trade('btc_usd',contract_type,curry_price,position,'1','1','20'))
        #         pass
        #     elif curry_price < IN_LOW:
        #         print(u'当前价格低于于进场价格,卖空')
        #         print(okcoinFuture.future_trade('btc_usd',contract_type,curry_price,position,'2','1','20'))
        #         pass
        #     else:
        #         print(u'等待入市信号')
        #         print(u'------')
        #         pass
    except Exception as e:
            print (e)
            continue
