# -*- coding: utf-8 -*-



BITMEX_PARAMS={
    'api_key':'336c441b896ecd0636bf46b0a3601f13',
    'SECRET_KEY':'5zZuDBjvswHc5VFPFGqXLGuzCDZZzGGSrOz3uaFCuJPZ8t0cF6XfOHa0loR8m0rw ',
    'URL':'test',
    'BTC_ADDRESS':''
}

BITMEX_ORDER_TYPE={'KD':'Buy',
               'KK':'Sell',
}

BITMEX_TRANSFER_TYPE={'E2F':1,
                  'F2E':2
}

BITMEX_API={
    #----makert api----
    'TICKER':('ticker','get'),
    'DEPTH':('depth','get'),
    'TRADES':('trades','get'),
    'KLINE':('kline','get'),
    #-----合约账户API--------
    'F_TICKER':('future_ticker','get'),
    'F_DEPTH':('future_depth','get'),
    'F_TRADES':('future_trades','get'),
    'F_INDEX':('future_index','get'),
    'EXCHANGE_RATE':('exchange_rate','get'),
    'F_EST_PRICE':('future_estimated_price','get'),
    'F_KLINE':('future_kline','get'),
    'F_H_AMOUNT':('future_hold_amount','get'),
    'F_PRICE_LIMIT':('future_price_limit','get'),

    #---------合约账户交易API-----------
    'F_USERINFO':('future_userinfo','post'),
    'F_POSITION':('future_position','post'),
    'F_TRADE':('future_trade','post'),
    'F_TRADES_HISTORY':('future_trades_history','post'),
    'F_BATCH_TRADE': ('future_batch_trade', 'post'),
    'F_CANCEL': ('future_cancel', 'post'),
    'F_ORDER_INFO': ('future_order_info', 'post'),
    'F_ORDERS_INFO': ('future_orders_info', 'post'),
    'F_USDERINFO_4FIX': ('future_userinfo_4fix', 'post'),
    'F_POSITION_4FIX': ('future_position_4fix', 'post'),
    'F_EXPLOSIVE': ('future_explosive', 'post'),
    'F_DEVOLVE': ('future_devolve', 'post'),


    #---trade api----
    'USERINFO':('userinfo','post'),
    'TRADE':('trade','post'),
    'BATCH_TRADE':('batch_trade','post'),
    'CANCEL_ORDER':('cancel_order','post'),
    'ORDER_INFO':('order_info','post'),
    'ORDERS_INFO':('orders_info','post'),
    'ORDER_HISTORY':('order_history','post'),
    'WITHDRAW':('withdraw','post'),
    'CANCEL_WITHDRAW':('cancel_withdraw','post'),
    'WITHDRAW_INFO':('withdraw_info','post'),
    'ACCOUNT_RECORDS':('account_records','post'),
}