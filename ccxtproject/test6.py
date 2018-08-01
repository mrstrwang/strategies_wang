#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import time
import json
import ccxt


bitz = ccxt.bitz()
apikey = bitz.apiKey = 'e08edbaef8fca9984a652e00386ec2e8'
secretkey = bitz.secret = 'HmctG3DcZyRONEA3d10wyPQ7LvYQbLToE1GFEh92MdvkvfHJaVk5DKgQYVgXoVe6'
bitz.password = 'vJ1cE1fB3rB7fF2'


class BITMEX_MAKER:

    def __init__(self,params):
        self._params = params
        self._BITMEXServices = bitz
        self.order_open_ID = ""

    def get_price_depth(self,symbol):
        '''
        #获取市场行情深度
        :param symbol:
        :return:
        '''
        sell=0.0000
        buy = 0.0000
        try:
            result = self._BITMEXServices.fetch_order_book(symbol)
            sell = result['asks'][-1][0]  #获取卖二价
            buy = result['bids'][0][0]   #获取买二价
            #print(result['asks'][-5:-1])
            #print(result['bids'][0:5])
        except Exception as e:
            print('error:%s'%e)
            return buy,sell
        finally:
            return buy,sell


    def deal_net_pot(self):
        print('test')

    def get_user_pot(self,symbol):
        '''
        获取用户仓位信息
        :param symbol:
        :return:
        '''
        result = self._BITMEXServices.fetch_balance()

        return result['info'][symbol]

    def check_risk(self,symbol):
        '''
        检查系统风险，实现仓位控制
        :param symbol:
        :return:
        '''
        risk = self.deal_net_pot(symbol)
        if risk['keep_deposit']/risk['account_rights'] <= self._params['risk_rate']:
            print('now risk is :%s,limit risk:%s'%(risk['keep_deposit']/risk['account_rights'],self._params['risk_rate']))
            return True
        else:
            print('now risk is :%s,limit risk:%s' % (risk['keep_deposit'] / risk['account_rights'], self._params['risk_rate']))
            return False

    def get_user_position(self,symbol):
        '''
        #获取仓位信息
        '''
        result={}
        result['status']=False
        try:
            holds = self._BITMEXServices.fetch_balance(({'filter': json.dumps({"symbol": symbol})}))
            for hold in holds:
                if symbol in hold['symbol']:
                    result['currentQty'] = hold['currentQty']#正负表示多空
                    print("品种:"+str(hold['symbol'])+";当前持仓:"+str(hold['currentQty']))
                    result['status'] = True
                elif  symbol not in hold :
                    continue
                else:
                    result['status'] = False

            return result
        except:
            raise

    def get_ma_data(self,symbol,period='1min',size = 60,contract_type='quarter'):

        data={}
        data['status']=False
        ma={}
        sum_5=0.0000
        sum_10=0.0000
        sum_15=0.0000
        sum_30=0.0000
        sum_60=0.0000
        try:
            result = self._BITMEXServices.fetch_ohlcv(symbol,period,size,contract_type)

            # df = pd.DataFrame(result)
            # df[0] = pd.to_datetime(df[0], unit='ms')
            # print (df.tail())
            if result:
                for i in range(0,size):
                    if i<5:
                        sum_5 = sum_5 + result[-1 - i][4] #获取收盘价
                    if i<10:
                        sum_10 = sum_10 + result[-1 - i][4]
                    if i<15:
                        sum_15 = sum_15 + result[-1 - i][4]
                    if i<30:
                        sum_30 = sum_30+ result[-1 - i][4]
                    if i<60:
                        sum_60 = sum_60 + result[-1 - i][4]

                ma['price'] = round(result[-1][4],4)
                ma['ma5'] = round(sum_5/5,4)
                ma['ma10'] = round(sum_10/10,4)
                ma['ma15'] = round(sum_15/15,4)
                ma['ma30'] = round(sum_30 / 30, 4)
                ma['ma60'] = round(sum_60 / 60, 4)
                data['status'] = True
                data['data'] = ma
        except Exception as e:
            data['status']=False

        return data

    def get_bollchannel_data(self,symbol,symbol_ccxt,period='1_m',size = 100):
        data={}
        data['status']=False
        boll={}
        n = self._params['n']
        try:
            limit = size
            now = self._BITMEXServices.milliseconds()
            period = period.split('_')  # 分钟数
            i = int(period[0])
            since = now - limit * i * 60 * 1000  # 当前时间之前多少毫秒数的K线,时间为UTC时间,与中国时间差8h
            result = self._BITMEXServices.fetch_ohlcv(symbol_ccxt,timeframe=period[0]+period[1],limit=size,since=since)
            df = pd.DataFrame(result)
            # df[0] = pd.to_datetime(df[0], unit='ms')
            # print (df.tail())
            if not df.empty:
                mid = round(df[4].mean(),4)
                std = round(df[4].std(),4)

                boll['price'] = round(result[-1][4])
                boll['upline'] = round((mid + n*std))
                boll['downline'] = round((mid - n*std))
                boll['midline'] = round(mid)
                boll['per'] = round((boll['upline']/boll['downline']-1),4)
                boll['n'] = self._params['n']
                boll['std'] = round(std)
                data['status'] = True
                data['data'] = boll
        except Exception as e:
            data['status']=False
        return data

    def get_trade_signal(self,symbol,symbol_ccxt,period='1_m',size = 100):

        result = BITMEX_maker.get_bollchannel_data(symbol,symbol_ccxt,period,size)
        if result['status']:

            if result['data']['price']>result['data']['upline'] and result['data']['per']>self._params['per']:
                result['signal'] = 1

            elif result['data']['price']<result['data']['downline'] and result['data']['per']>self._params['per']:
                result['signal'] = -1

            else:result['signal'] = 0
        else:
            result['status'] = False

        return result

    def get_wt_orders(self,symbol):
        '''
        #获取用户活动委托订单类型
        :param symbol:
        :return:
        '''
        return_data={}
        wt_list=[]
        wt_orders = self._BITMEXServices.private_get_order(({'filter': json.dumps({"open": True,"symbol": symbol})}))
        if wt_orders:
            for order in wt_orders:
                wt_list.append(order['orderID'])
            return_data['orders']=wt_orders
            return_data['orders_list'] = wt_list

        return return_data  # 返回用户委托订单类型

    def send_pc_orders(self,symbol,symbol_ccxt,signal):
        #print('用户持仓数据： %s' % position)
        #print('signal数据：%s'%signal_data)
        order_info = {}
        user_pos = self.get_user_position(symbol)
        if user_pos['status']:
            #print('交易信号:%s'%signal['signal'])
            wt_orders = self.get_wt_orders(symbol)
            # ------------------------------------平空-----------------#
            if wt_orders:
                if signal['data']['price'] > signal['data']['midline'] :
                    if user_pos['currentQty']<0 and self.order_open_ID not in wt_orders['orders_list']:
                        pk_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'buy', user_pos['currentQty'])
                        self.order_open_ID = pk_order['id']
                        print(pk_order)
                        if pk_order:
                            order_info = pk_order
                            print('执行空头平仓(市价)：%s' % pk_order)
            else:
                if signal['data']['price'] > signal['data']['midline'] :
                    if user_pos['currentQty']<0 :
                        pk_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'buy', user_pos['currentQty'])
                        self.order_open_ID = pk_order['id']
                        print(pk_order)
                        if pk_order:
                            order_info = pk_order
                            print('执行空头平仓(市价)：%s' % pk_order)

            #------------------------------------平多-----------------#
            if wt_orders:
                if signal['data']['price'] < signal['data']['midline']:
                    if user_pos['currentQty']>0 and  self.order_open_ID not in wt_orders['orders_list']:
                        pd_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'sell', user_pos['currentQty'])
                        self.order_open_ID = pd_order['id']
                        print(pd_order)
                        if pd_order:
                            order_info = pd_order
                            print('执行多头平仓(市价)：%s' % pd_order)
            else:
                if signal['data']['price'] < signal['data']['midline']:
                    if user_pos['currentQty']>0 :
                        pd_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'sell', user_pos['currentQty'])
                        self.order_open_ID = pd_order['id']
                        print(pd_order)
                        if pd_order:
                            order_info = pd_order
                            print('执行多头平仓(市价)：%s' % pd_order)

        return order_info

    def send_kc_orders(self,symbol,symbol_ccxt,signal):

        order_info={}
        user_pos = self.get_user_position(symbol)
        if user_pos['status']:
            print('交易信号:%s' % signal['signal'])
            # --------------------------------------开多-----------------------------------
            wt_orders=self.get_wt_orders(symbol)
            if signal['signal'] == 1:
                if wt_orders:
                    if user_pos['currentQty'] == 0 and self.order_open_ID not in wt_orders['orders_list']:
                        buy_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'buy', self._params['amount'])
                        self.order_open_ID = buy_order['id']

                        if buy_order:
                            order_info = buy_order
                            print('多头已下单(市价):%s' % buy_order)
                else:
                    if user_pos['currentQty'] == 0:
                        buy_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'buy',self._params['amount'])
                        self.order_open_ID = buy_order['id']

                        if buy_order:
                            order_info = buy_order
                            print('多头已下单(市价):%s' % buy_order)

            # --------------------------------------开空-----------------------------------
            elif signal['signal'] == -1:
                if wt_orders:
                    if user_pos['currentQty'] == 0 and self.order_open_ID not in wt_orders['orders_list'] :
                        sell_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'sell', self._params['amount'])
                        self.order_open_ID = sell_order['id']
                        if sell_order:
                            order_info = sell_order
                            print('空头已下单(市价):%s' % sell_order)
                else:
                    if user_pos['currentQty'] == 0 :
                        sell_order = self._BITMEXServices.create_order(symbol_ccxt, 'market', 'sell', self._params['amount'])
                        self.order_open_ID = sell_order['id']
                        if sell_order:
                            order_info = sell_order
                            print('空头已下单(市价):%s' % sell_order)

        return order_info

    def trade_system(self,symbol,symbol_ccxt,period='1_m',size=60):

        try:
            signal = self.get_trade_signal(symbol,symbol_ccxt, period, size)  # 获取行情交易信号
            if signal['status']:#获取到交易信号
                pc_order = self.send_pc_orders(symbol,symbol_ccxt, signal)  #处理平仓
                if pc_order:
                    print("平仓订单:%s"%pc_order)
                kc_order = self.send_kc_orders(symbol,symbol_ccxt, signal)  #处理开仓
                if kc_order:
                    print("开仓订单:%s"%kc_order)
                print(signal)
        except:
            raise

if __name__ == '__main__':
    params ={}
    params['amount'] =10
    params['n'] = 2.7
    params['per']  =0.35
    BITMEX_maker = BITMEX_MAKER(params)
    symbol = 'BZ/USDT'
    symbol_ccxt = 'BZ/USDT'

    #主循环模块
    while True:
        BITMEX_maker.trade_system(symbol,symbol_ccxt,'5_m',size= 360)
        time.sleep(15)

    #测试get数据功能
    # tmp = BITMEX_maker.get_bollchannel_data(symbol,'5_m',size= 120)
    # print (tmp)

    #测试get仓位功能
    # tmp = BITMEX_maker.get_user_position(symbol)
    # print (tmp)

    # 测试get订单功能
    # tmp = BITMEX_maker.get_wt_orders(symbol)
    # print (tmp)

