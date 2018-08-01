#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.settings import BITMEX_PARAMS
import ccxt
# import bitmex
# # import datetime
# # import pandas as pd
# # import json

def connection():
    bitz = ccxt.bitz()
    bitz.apiKey = BITMEX_PARAMS['api_key']
    bitz.secret = BITMEX_PARAMS['SECRET_KEY']
    #区分是否使用了测试连接
    # if BITMEX_PARAMS['URL'] == 'test':
    #     bitz.urls["api"] = bitz.urls["test"]
    #print(bitmex.fetch_balance())
    return bitz




if __name__ == '__main__':

    bitmex = connection()


    #1 fetchMarkets ()：获取从交易所所有可用的市场列表并返回市场的阵列（具有如属性的对象symbol，base，quote等等）。
    # 有些交易所无法通过在线API获取市场清单。对于那些，市场的名单是硬编码的。
    # result = bitmex.fetch_markets()
    # print(result)

    #2 loadMarkets ([reload])：将市场列表作为由符号索引的对象返回并用交换实例对其进行缓存。
    # 如果已加载，则返回缓存的市场，除非reload = true标志被强制。
    # 可交易品种:'.XRPXBT': {'precision': {}, 'limits': {}, 'id': '.XRPXBT', 'symbol': '.XRPXBT', 'base': 'XRP', 'quote': 'BTC', 'active': False, 'taker': None,
    # result = bitmex.load_markets(reload=True)
    # print(result)

    #3 fetchOrderBook (symbol[, limit = undefined[, params = {}]])：获取特定市场交易代码的L2 / L3订单。
    # result = bitmex.fetch_order_book("BTC/USD")
    # print(result)

    #4 fetchTrades (symbol[, since[, [limit, [params]]]])：获取特定交易代码的近期交易。
    # result = bitmex.fetch_trades("BTC/USD")
    # print(result)

    #5 fetchTicker (symbol)：获取tick数据。
    # result = bitmex.fetch_ticker("BTC/USD")
    # print(result)

    #6 fetchBalance ()：帐户信息。
    # result = bitmex.fetch_balance()
    # print(result)

    #7 fetch_ohlcv ():获取K线数据
    # limit =100
    # now = bitmex.milliseconds()
    # i = 1 #分钟数
    # since = now - limit * i * 60 * 1000 #当前时间之前多少毫秒数的K线,时间为UTC时间,与中国时间差8h
    # df = pd.DataFrame(bitmex.fetch_ohlcv("BTC/USD", timeframe=str(i)+"m", limit=limit, since=since))
    # df[0] = pd.to_datetime(df[0], unit='ms')
    # print (df.tail())

    #8 私有API方法
    print(dir(bitmex))#打印所有私有方法和公有方法

    #9 获取持仓信息
    # tmp = bitmex.private_get_position()
    # print(tmp)

    #10 获取订单信息(活动的)
    # symbol = "XBTUSD"
    # #tmp = bitmex.private_get_order(({'filter': json.dumps({"open": True,"symbol": symbol})}))
    # tmp = bitmex.private_get_order()
    # print(tmp)

    # 11 发送订单
    # symbol = 'BTC/USD'  # bitcoin contract according to bitmex futures coding
    # type = 'market'  # or 'market', or 'Stop' or 'StopLimit'
    # side = 'sell'  # or 'buy'
    # amount = 1.0
    # price = 6500.0  # or None extra params and overrides
    # params = {
    #     'stopPx': 6000.0,  # if needed
    # }
    # order = bitmex.create_order(symbol, type, side, amount)
    # print(order)

    #12 一次发出多个订单
    # orders = json.dumps([
    #     {"symbol": "XBTUSD", "side": "Sell", "orderQty": 1, "price": 9999},
    #     {"symbol": "XBTUSD", "side": "Sell", "orderQty": 1, "price": 9977}
    # ])
    # result = bitmex.private_post_order_bulk(({'orders': orders}))
    # print(result)

    #13 退出登录
    # tmp=bitmex.private_post_user_logout()
    # print(tmp)
    # createOrder(symbol, type, side, amount[, price[, params]])
    # createLimitBuyOrder(symbol, amount, price[, params])
    # createLimitSellOrder(symbol, amount, price[, params])
    # createMarketBuyOrder(symbol, amount[, params])
    # createMarketSellOrder(symbol, amount[, params])
    # cancelOrder(id[, symbol[, params]])
    # fetchOrder(id[, symbol[, params]])
    # fetchOrders([symbol[, params]])
    # fetchOpenOrders([symbol[, params]])
    # fetchClosedOrders([symbol[, params]])

