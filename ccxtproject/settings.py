BITMEX_ORDER_TYPE={'KD':'Buy',
               'KK':'Sell',
}

BITMEX_TRANSFER_TYPE={'E2F':1,
                  'F2E':2
}

BITMEX_API={
    #----makert api----
    'TICKER':('ticker','get'),  #获取牌价数据
    'DEPTH':('depth','get'),    #获取深度数据
    'ORDERS':('orders','get'),  #获取成交单
    'TICKERALL':('tickerall','get'), #获取所有牌价数据
    'KLINE':('kline','get'),    #获取k线数据

    #---trade api----
    'TRADEADD':('tradeAdd','post'),  #提交委托单
    'OPENORDERS':('openOrders','post'), #获取我的委托单
    'TRADECANCEL':('tradeCancel','post'), #撤销委托单
    'BALANCES':('balances','post'),   #我的资产
}
