
import ccxt
import pandas as pd
import numpy as np
import datetime
import time


# 引入初始信息
bitz = ccxt.bitz()
apikey = bitz.apiKey = ''
secretkey = bitz.secret = ''
# bitz.password = ''
bitz.password = ''

balance = bitz.fetch_balance()['BZ']   # 获取用户的BZ余额信息



# 获取并整理数据
def cut(deep):
    deep['bid_price'] = ''  # 卖出价格
    deep['bid_volume'] = ''  # 卖出数量
    deep['ask_price'] = ''  # 买入价格
    deep['ask_volume'] = ''  # 买入数量

    for i in range(len(deep)):  # 获取当前货币对的数量,进行数据交换
        deep.ix[i, 'bid_price'] = deep.ix[i, 'bids'][0]  # ix是pandas中的索引方法,它是一种混合索引
        deep.ix[i, 'bid_volume'] = deep.ix[i, 'bids'][1]
        deep.ix[i, 'ask_price'] = deep.ix[i, 'asks'][0]
        deep.ix[i, 'ask_volume'] = deep.ix[i, 'asks'][1]
    del deep['asks']  # 删除买入的缓存价格,以便下一次价格存入
    del deep['bids']  # 删除卖出的缓存价格,以便下一次价格存入
    # 将获取的买入、卖出数据放到deep中,并且精确到4位小数
    deep['bid_price'] = deep['bid_price'].astype('float64')
    deep['bid_volume'] = deep['bid_volume'].astype('float64')
    deep['ask_price'] = deep['ask_price'].astype('float64')
    deep['ask_volume'] = deep['ask_volume'].astype('float64')
    return deep  # 返回市场深度数据


# 这是一个数量差（为什么是前10个卖出的数量和倒数10个买入的数量）
def bid_ask_vol_diff(deep):
    bidvol10 = deep['bid_volume'][:10]  # 获取前10个卖出的数量
    askvol10 = deep['ask_volume'][-10:]  # 获取倒数10个买入的数量
    diff = bidvol10.sum() - askvol10.sum()  # 计算出买入和卖出的数量差
    return diff  # 返回数量差


# 这是一个卖出和买入的价格差，
def bid_ask_price_diff(deep):
    bidprice10 = deep['bid_price'][:10]  # 获取前10个卖出的价格
    askprice10 = deep['ask_price'][-10:]  # 获取倒数10个买入的数量
    bid_diff = bidprice10.max() - bidprice10.min()  # 获取到卖出的最大价格差
    ask_diff = askprice10.max() - askprice10.min()  # 获取到买入的最大价格差
    diff = bid_diff - ask_diff  # 计算出卖出和买入的最大价格差
    return diff  # 返回价格差


# 这是返回的布尔值，当卖出数量大于买入数量为1。
def bid_ask_bigvol(deep):
    bidvol10 = deep['bid_volume'][:10]  # 获取前10个卖出的数量
    askvol10 = deep['ask_volume'][-10:]  # 获取倒数10个买入的数量
    diff = bidvol10.max() > askvol10.max()  # 当diff大于bidvol10.max()则返回1，否则返回0
    return diff


i = 0  # i为零时表示开始交易


while True:

    deep = pd.DataFrame(bitz.fetch_order_book('BZ/USDT'))  # 将货币对深度数据转换成二维数组
    deep = cut(deep)  # 整理数据


    if bid_ask_vol_diff(deep) > 0 and bid_ask_price_diff(deep) < 0 and bid_ask_bigvol(deep) > 0:
        price_buy = str(deep['bid_price'][1]+0.0001)  # 如果条件满足,在原有的购买价格上加0.0001作为现有的价格
        print('=========', price_buy)
        # 创建一个买的订单
        buy = bitz.create_order(symbol='BZ/USDT', type='limit', side='buy', amount=1, price=price_buy)

    time.sleep(5)  # 让服务器休息一会
    price_sell = str(deep['bid_price'][1]+0.5)  # 如果条件不满足，则在原有卖出的价格上加0.5
    # 创建一个卖的订单
    sell = bitz.create_order('BZ/USDT', type='limit', side='sell', amount=1, price=price_sell)
    i = i+1   # 交易完成，自动下一次交易

    try:
        # 获取到委托单id
        orders = bitz.fetch_open_orders('BZ/USDT')  # 获取所有的订单
        for _ in range(len(orders)):  # 获取到订单数

            # print(orders[i]['side'])
            if orders[_]['side'] == 'sale':  # 判断当前订单是否是卖
                sellid = orders[_]['id']  # 如果当前订单是卖，则获取它的id
                print('sellid', sellid)
                time.sleep(5)   # 等待5秒后如果没有成交则撤销订单
                cancel_sell = bitz.cancel_order(id=sellid, symbol='BZ/USDT')
            elif orders[_]['side'] == 'buy':  # 判断当前订单是否是买
                buyid = orders[_]['id']  # 如果是买，则获取到它的id
                print('buyid', buyid)
                time.sleep(5)   # 等待5秒后如果没有成交则撤销订单
                cancel_buy = bitz.cancel_order(id=buyid, symbol='BZ/USDT')
            else:
                pass
    except NameError:
        pass
    except KeyError:
        pass
    # time.sleep(5)
    # try:
    #     cancel_buy = bitz.cancel_order(id=buyid,symbol='BZ/USDT')
    #     cancel_sell = bitz.cancel_order(id=sellid,symbol='BZ/USDT')
    # except NameError:
    #     pass
    # except KeyError:
    #     pass
    # 获取账户余额
    info_bz_free = balance['total']
    # info_bz_free = bitz.fetch_ticker('BZ/USDT')['info']

    print('第%s次交易,账户bz币余额:%s' % (i, info_bz_free))


