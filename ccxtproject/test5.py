from OkcoinSpotAPI import *
import pandas as pd
import numpy as np
import datetime
import time

######################################################初始数据
# 引入初始信息
apikey = '9b93e53a-e803-4883-b8fc-64af2f3ccc57'
secretkey = '14284B3C0B9CF0F932E83888388855C9'
okcoinRESTURL = 'www.okcoin.cn'  # 请求注意：国内账号需要 修改为 www.okcoin.cn
okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)
okcoinFuture = OKCoinFuture(okcoinRESTURL, apikey, secretkey)


# info=eval(okcoinSpot.userinfo())#账户信息
# info
#####################################获取并整理数据
def cut(deep):
    deep['bid_price'] = ''
    deep['bid_volume'] = ''
    deep['ask_price'] = ''
    deep['ask_price'] = ''
    for i in range(len(deep)):
        deep.ix[i, 'bid_price'] = deep.ix[i, 'bids'][0]
        deep.ix[i, 'bid_volume'] = deep.ix[i, 'bids'][1]
        deep.ix[i, 'ask_price'] = deep.ix[i, 'asks'][0]
        deep.ix[i, 'ask_volume'] = deep.ix[i, 'asks'][1]
    del deep['asks']
    del deep['bids']
    deep['bid_price'] = deep['bid_price'].astype('float64')
    deep['bid_volume'] = deep['bid_volume'].astype('float64')
    deep['ask_price'] = deep['ask_price'].astype('float64')
    deep['ask_price'] = deep['ask_price'].astype('float64')
    return deep


def bid_ask_vol_diff(deep):
    bidvol10 = deep['bid_volume'][:10]
    askvol10 = deep['ask_volume'][-10:]
    diff = bidvol10.sum() - askvol10.sum()
    return diff  # diff>0是入场条件1


def bid_ask_price_diff(deep):
    bidprice10 = deep['bid_price'][:10]
    askprice10 = deep['ask_price'][-10:]
    bid_diff = bidprice10.max() - bidprice10.min()
    ask_diff = askprice10.max() - askprice10.min()
    diff = bid_diff - ask_diff  # 小于0是入场条件
    return diff


def bid_ask_bigvol(deep):
    bidvol10 = deep['bid_volume'][:10]
    askvol10 = deep['ask_volume'][-10:]
    diff = bidvol10.max() > askvol10.max()  # 大于0是入场条件
    return diff


i = 0
while True:

    deep = pd.DataFrame(okcoinSpot.depth('btc_cny')) #获取OKCOIN现货市场深度信息
    deep = cut(deep)
    deep
    if bid_ask_vol_diff(deep) > 0 and bid_ask_price_diff(deep) < 0 and bid_ask_bigvol(deep) > 0:
        price_buy = str(deep['bid_price'][1] + 0.01)
        buy = okcoinSpot.trade('btc_cny', 'buy', price_buy, '0.01')    #现货交易

    time.sleep(0.2)
    price_sell = str(deep['bid_price'][1] + 0.50)
    sell = okcoinSpot.trade('btc_cny', 'sell', price_sell, '0.01')   #现货交易
    print(sell)
    i = i + 1
    try:
        buyid = str(eval(buy)['order_id'])
        sellid = str(eval(sell)['order_id'])
    except NameError:
        pass
    except KeyError:
        pass
    time.sleep(5)
    try:
        cancel_buy = okcoinSpot.cancelOrder('btc_cny', buyid)   #现货取消订单
        cance1_sell = okcoinSpot.cancelOrder('btc_cny', sellid) #现货取消订单
    except NameError:
        pass
    except KeyError:
        pass
    info_btc_free = eval(eval(okcoinSpot.userinfo())['info']['funds']['free']['btc'])
    info_net = eval(eval(okcoinSpot.userinfo())['info']['funds']['asset']['net'])
