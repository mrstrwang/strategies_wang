
import ccxt
import pandas as pd
import numpy as np
import datetime
import time
import random

# 引入初始信息
bitz = ccxt.bitz()
apikey = bitz.apiKey = 'e08edbaef8fca9984a652e00386ec2e8'
secretkey = bitz.secret = 'HmctG3DcZyRONEA3d10wyPQ7LvYQbLToE1GFEh92MdvkvfHJaVk5DKgQYVgXoVe6'
bitz.password = 'bX1gF6cF1cH7bD3'

balance = bitz.fetch_balance()['BZ']   # 获取用户的BZ余额信息
print('balance', balance)

# 获取 bz的free信息
info_bz_free = bitz.fetch_ticker('BZ/USDT')['info']

# 创建一个记录卖单的最低价格和一个买的最高价格
bid_big_price = ''
ask_big_price = ''


# 获取深度信息并进行整理
def cut():
    deep = pd.DataFrame(bitz.fetch_order_book('BZ/USDT'))
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
    bid_vol_10 = deep['bid_volume'][:15]  # 这是买入的前十个从高到低
    ask_vol_10 = deep['ask_volume'][:15]  # 这是卖出的前十个从低到高
    diff = bid_vol_10.sum() - ask_vol_10.sum()  # 这里为什么是数量，数量怎么会成为考量之一
    return diff  # 总的数量


# 这是一个卖出和买入的价格差，
def bid_ask_price_diff(deep):
    bid_price_10 = deep['bid_price'][:15]  # 买入的前十个从高到低
    ask_price_10 = deep['ask_price'][:15]  # 卖出的前十个从低到高
    bid_diff = bid_price_10.max() - bid_price_10.min()  # 在买如的最大价格减去最小的价格
    ask_diff = ask_price_10.max() - ask_price_10.min()  # 在卖出的最大价格减去最小的价格
    diff = bid_diff - ask_diff  # 买入的的价格差-卖出的价格差
    return diff


# 这是返回的布尔值，当卖出数量大于买入数量为1。
def bid_ask_bigvol(deep):
    bid_vol_10 = deep['bid_volume'][:15]  # 买进的前十个从高到底
    ask_vol_10 = deep['ask_volume'][:15]  # 卖出的前十个从低到高
    diff = bid_vol_10.max() > ask_vol_10.max()
    return diff


# 返回的为布尔值，当卖出的最低价大于买进的最高价时返回True
def bid_ask_big_price(deep):
    bid_pri_10 = deep['bid_price'][:15]  # 买进的前十个从高到底
    ask_pri_10 = deep['ask_price'][:15]  # 卖出的前十个从低到高
    diff = bid_pri_10.max() < ask_pri_10.min() - 0.0006  # 买进的最高价小于卖出最低价-买卖的税
    return diff


# 创建买单
def create_bid(deep):
    # 当买入总数量大于卖出数量，并且买入的价格小于卖出的价格差，并且买入的最大数量大于卖出的最大数量时
    # bid_ask_vol_diff(deep) > 0 and bid_ask_price_diff(deep) < 0 and bid_ask_bigvol(deep) > 0
    if bid_ask_vol_diff(deep) > 0 and bid_ask_price_diff(deep) < 0 and bid_ask_big_price(deep) == 1:
        print('即将创建买单')
        # 创建买的价钱字符段，然后随机选择加上0到0.0003的价格
        price_buy = str(deep['bid_price'][0] + random.choice([0, 0.0001, 0.0002, 0.0003]))
        print('price_buy', price_buy)
        # 创建一个买的订单
        bitz.create_order(symbol='BZ/USDT',
                          type='limit',
                          side='buy',
                          amount=balance['total'] / 100 * random.uniform(1, 10),
                          price=price_buy)


# 创建卖单
def create_ask(deep):
    if balance['total'] > 0 and bid_ask_big_price(deep) == 1:
        print('即将创建卖单')
        price_sell = str(deep['ask_price'][0] - random.choice([0, 0.0001, 0.0002, 0.0003]))
        print('price_sell', price_sell)
        # 创建一个卖的订单，后随机选择减去0到0.0003的价格
        bitz.create_order('BZ/USDT',
                          type='limit',
                          side='sell',
                          amount=balance['total'] / 100 * random.uniform(1, 10),
                          price=price_sell)


i = 0
j = 0
while True:
    try:
        # 获取到委托单id
        orders = bitz.fetch_open_orders('BZ/USDT')  # 获取所有买入的委托
        print('委托的单数%s' % len(orders))
        deep = cut()  # 提供深度路径
        print(orders)
        time.sleep(5)
        if len(orders) == 0:  # 查找有没有订单没有则创建，有则进行下一步判断
            print('没有订单')
            bid_big_price = deep['bid_price'][0]  # 记录买盘价钱
            create_bid(deep)  # 创建买盘
            time.sleep(5)
            ask_big_price = deep['ask_price'][0]  # 记录卖盘价钱
            create_ask(deep)  # 创建卖盘
            time.sleep(5)
        elif len(orders) == 1 and orders[0]['side'] == 'sale':  # 如果只有一个买单，则创建卖单
            bid_big_price = deep['bid_price'][0]  # 记录买盘价钱
            create_bid(deep)  # 创建买盘
            time.sleep(5)
        elif len(orders) == 1 and orders[0]['side'] == 'buy':  # 如果只有一个卖单，则创建一个买单
            ask_big_price = deep['ask_price_price'][0]  # 记录买盘价钱
            create_ask(deep)  # 创建买盘
            time.sleep(5)
        elif len(orders) >= 3:  # 如果超过3个单子则都撤单
            for _ in range(len(orders)):  # 获取到订单数
                if orders[_]['side'] == 'sale':  # 判断当前订单是否是卖
                    sell_id = orders[_]['id']  # 如果当前订单是卖，则获取它的id
                    cancel_sell = bitz.cancel_order(id=sell_id, symbol='BZ/USDT')
                    time.sleep(5)
                elif orders[_]['side'] == 'buy':  # 判断当前订单是否是买
                    buy_id = orders[_]['id']  # 如果是买，则获取到它的id
                    cancel_buy = bitz.cancel_order(id=buy_id, symbol='BZ/USDT')
                    time.sleep(5)
        else:
            print('orders订单信息为：', orders)
            for _ in range(len(orders)):  # 获取到订单数
                # print(orders[i]['side'])
                if orders[_]['side'] == 'sale':  # 判断当前订单是否是卖
                    sell_id = orders[_]['id']  # 如果当前订单是卖，则获取它的id
                    print('sell_id', sell_id)
                    ask_price = deep['ask_price'][1]
                    if ask_big_price == ask_price:
                        i += 1
                        time.sleep(5)
                        pass
                    else:
                        time.sleep(5)
                        cancel_sell = bitz.cancel_order(id=sell_id, symbol='BZ/USDT')
                        time.sleep(5)  # 等待网页一会，谨防在自己的卖单上做运算
                        create_ask(deep)  # 创建卖盘
                        time.sleep(5)
                elif orders[_]['side'] == 'buy':  # 判断当前订单是否是买
                    buy_id = orders[_]['id']  # 如果是买，则获取到它的id
                    print('buy_id', buy_id)
                    bid_price = deep['bid_price'][1]
                    if bid_big_price == bid_price:
                        j += 1
                        time.sleep(5)
                        pass
                    else:
                        time.sleep(5)   # 等待5秒后如果没有成交则撤销订单
                        cancel_buy = bitz.cancel_order(id=buy_id, symbol='BZ/USDT')
                        time.sleep(5)
                        create_bid(deep)  # 创建买盘
                        time.sleep(5)
                else:
                    time.sleep(5)
        print('卖盘', i)
        print('买盘', j)
        if i > 10:
            ask_big_price = ''
            i = 0
        if j > 10:
            bid_big_price = ''
            j = 0

    except Exception as e:
        print('e', e)
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
    # info_bz_free = balance['total']
    # info_bz_free = bitz.fetch_ticker('BZ/USDT')['info']
    print('账户bz币余额:%s' % info_bz_free)
    # 保持历史的最后一个小时在高速缓存
    before = bitz.milliseconds() - 1 * 60 * 60 * 1000
    # 清除所有已关闭和取消的订单'较旧'或在'之前'发出
    bitz.purge_cached_orders(before)

    time.sleep(5)