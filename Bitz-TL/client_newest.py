import random
import time
import settings
import asyncio
import ccxt.async_support as ccxt_01
import ccxt
import logging
# 日志
# logging.basicConfig(level=logging.DEBUG,filename='/Users/admin/Desktop/bitz/loggmsg.log')
# URL
api = settings.BITZ_API
# KEY\SER
exchange = ccxt.bitz({
    'apiKey': settings.CONSTANT_KEY_BITZ,
    'secret': settings.CONSTANT_SECRET_BITZ,
})
while True:
    """
    如果，买卖执行完了 ，系统会抛出异常， 为了让程序继续运转使用try
    """
    try:
        # 使用异步获取动态数据
        async def print_poloniex_ethbtc_ticker():
        # 实现自动买卖功能
            while True:
                # 1。实现异步
                poloniex = ccxt_01.bitz({
                'apiKey': settings.CONSTANT_KEY_BITZ,
                'secret': settings.CONSTANT_SECRET_BITZ,
                })
                await asyncio.sleep(1)
                # 获取实时成交行情USDT|ETH
                DATA=(await poloniex.fetch_ticker('BZ/USDT'))
                DATA1 = (await poloniex.fetch_ticker('BZ/ETH'))


                DATA3=(await poloniex.fetch_ticker('BZ/USDT'))
                DATA4 = (await poloniex.fetch_ticker('BZ/ETH'))
                # ETH中间转化
                intermediate_variable= (await poloniex.fetch_ticker('ETH/USDT'))
                # 2。获取商户的信息私有
                DATA_pos = (await poloniex.fetch_balance())
                # BZ_DATA_POS=DATA_pos['BZ']['free']
                # 买
                USDT_bid_DATA=DATA['bid']
                # print(USDT_bid_DATA)
                # 卖
                USDT_ask_DATA=DATA['ask']
                # 买
                ETH_bid_DATA=DATA1['bid']
                # 卖
                ETH_ask_DATA = DATA1['ask']
                # usdt区BZ的最新价格
                USDT_close_DAT=DATA3['close']
                # ETH区BZ的最新价格
                ETH_close_DAT=DATA4['close']
                # ETH中间转化
                ETH_USDT_ZH=intermediate_variable['last']
                # # # # 查询BZ账户货币对的持仓数量     账户持仓币种数量
                BZ_DATA_POS = DATA_pos['BZ']['free']
                # # # 查询ETH账户货币对的持仓
                BZ_ETH_pos = DATA_pos['ETH']['free']
                # # # 查询USDT账户货币对的持仓
                BZ_USDT_pos = DATA_pos['USDT']['free']
                # # # 转化后的币种
                ETH_dict =ETH_bid_DATA *ETH_USDT_ZH
                ETH_dict_bid=ETH_bid_DATA *ETH_USDT_ZH
                #
                ETH_dict_ask=ETH_ask_DATA *ETH_USDT_ZH
                # EHT区最新BZ价格转换为USDT的价格
                ETH_BZ_ZH_USDT_JG = ETH_close_DAT * ETH_USDT_ZH

                # # # 第一次市价买入或卖出货币对数量
                Number_market_BZ = ( BZ_DATA_POS  * 0.02)
                Number_market_USDT = (BZ_USDT_pos * 0.02)

                # 数量转换指引if判断
                Number_market_USDT_BID_BZ=(Number_market_USDT/USDT_bid_DATA)
                Number_market_ETH_BID_BZ=(BZ_ETH_pos/ETH_bid_DATA)
                # 随机数量
                Number_market_USDT_BID_BZ_UNIFORM=random.uniform(1,Number_market_USDT_BID_BZ)

                Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL=random.uniform(1,Number_market_BZ)
                # ETH区eth币每次可买入bz币的数量
                Number_market_ETH = (Number_market_ETH_BID_BZ * 0.02)
                # 随机数
                Number_market_ETH_BUY=random.uniform(1,Number_market_ETH)
                # 价格的转换
                # 市场价格
                #                                    3.进行判断
                """
                如果USDT价格小于ETH 且（ETH减去USDT的价格）/USDT价格>0.00001=
                """
                if USDT_close_DAT<ETH_BZ_ZH_USDT_JG and (ETH_BZ_ZH_USDT_JG - USDT_close_DAT)/USDT_close_DAT > 0.00001:
                    # time.sleep(3)
                    # 第二次建仓价格
                    Second_building_prices = USDT_bid_DATA * 0.9
                    Second_building_prices3 = USDT_bid_DATA * 0.8
                    Second_building_prices4 = USDT_bid_DATA * 0.7
                    Second_building_prices5 = USDT_bid_DATA * 0.6
                    Second_building_prices6 = USDT_bid_DATA * 0.5
                    # 1    可买货币的数量 * 2 %= 实时成交价格，卖一价市场价格      市价订单可买货币的数量 * 2 %
                    if BZ_USDT_pos>0:
                        #如果 上面的条件成立，我执行创建市价单，如果市价单抛出异常，我就捕获异常 跳出本次异常，继续循环，知道条件条件满足
                        print('1')
                    try:
                                                                                                                                    # 价格必须低于市价不能高于和等于市价
                        print(await poloniex.create_order(symbol='BZ/USDT', side='buy', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM, price=USDT_bid_DATA+0.0001))
                    except Exception:
                        continue
                    else:
                        print(await poloniex.create_order(symbol='BZ/USDT', side='buy', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM, price=Second_building_prices))  ## 限价订单
                        print(await poloniex.create_order(symbol='BZ/USDT', side='buy', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM, price=Second_building_prices3))
                        print(await poloniex.create_order(symbol='BZ/USDT', side='buy', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM, price=Second_building_prices4))
                        print(await poloniex.create_order(symbol='BZ/USDT', side='buy', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM, price=Second_building_prices5))
                        print(await poloniex.create_order(symbol='BZ/USDT', side='buy', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM, price=Second_building_prices6))
                        # # # USDT账户货币对的持仓>0
                        if BZ_ETH_pos>0:
                            # 第二次建仓价格
                            Second_building_prices =  ETH_ask_DATA * 1.1
                            Second_building_prices3 = ETH_ask_DATA * 1.2
                            Second_building_prices4 = ETH_ask_DATA * 1.3
                            Second_building_prices5 = ETH_ask_DATA * 1.4
                            Second_building_prices6 = ETH_ask_DATA * 1.5
                            # 提交订单
                        #如果 上面的条件成立，我执行创建市价单，如果市价单抛出异常，我就捕获异常 跳出本次异常，继续循环，知道条件条件满足
                        try:
                            print(await poloniex.create_order(symbol='BZ/ETH', side='sell', type='limt',amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=ETH_ask_DATA-0.000000001))
                        except Exception:
                            continue
                        else:
                            print(await poloniex.create_order(symbol='BZ/ETH', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices))
                            print(await poloniex.create_order(symbol='BZ/ETH', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices3))
                            print(await poloniex.create_order(symbol='BZ/ETH', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices4))
                            print(await poloniex.create_order(symbol='BZ/ETH', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices5))
                            print(await poloniex.create_order(symbol='BZ/ETH', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices6))
                            continue
                elif USDT_close_DAT > ETH_BZ_ZH_USDT_JG and (USDT_close_DAT-ETH_BZ_ZH_USDT_JG)/ETH_BZ_ZH_USDT_JG > 0.00001:
                    Second_building_prices2 = ETH_bid_DATA * 0.9
                    Second_building_prices3 = ETH_bid_DATA * 0.8
                    Second_building_prices4 = ETH_bid_DATA * 0.7
                    Second_building_prices5 = ETH_bid_DATA * 0.6
                    Second_building_prices6 = ETH_bid_DATA * 0.5
                    if BZ_ETH_pos>0:
                        print('1')
                        # 如果 上面的条件成立，我执行创建市价单，如果市价单抛出异常，我就捕获异常 跳出本次异常，继续循环，知道条件条件满足
                    try:
                        print('--------1')                                                                                  # 价格必须低于市价不能高于和等于市价
                        print(await poloniex.create_order(symbol='BZ/ETH', side='buy', type='limt', amount=Number_market_ETH_BUY,price=ETH_bid_DATA+0.000000001))
                    except Exception:
                        continue
                    else:
                        print(await poloniex.create_order(symbol='BZ/ETH', side='buy', type='limt', amount=Number_market_ETH_BUY, price=Second_building_prices2))
                        print(await poloniex.create_order(symbol='BZ/ETH', side='buy', type='limt', amount=Number_market_ETH_BUY, price=Second_building_prices3))
                        print(await poloniex.create_order(symbol='BZ/ETH', side='buy', type='limt', amount=Number_market_ETH_BUY, price=Second_building_prices4))
                        print(await poloniex.create_order(symbol='BZ/ETH', side='buy', type='limt', amount=Number_market_ETH_BUY, price=Second_building_prices5))
                        print(await poloniex.create_order(symbol='BZ/ETH', side='buy', type='limt', amount=Number_market_ETH_BUY, price=Second_building_prices6))

                        if BZ_USDT_pos>0:
                            Second_building_prices2 = USDT_ask_DATA * 1.1
                            Second_building_prices3 = USDT_ask_DATA * 1.2
                            Second_building_prices4 = USDT_ask_DATA * 1.3
                            Second_building_prices5 = USDT_ask_DATA * 1.4
                            Second_building_prices6 = USDT_ask_DATA * 1.5
                        # 如果 上面的条件成立，我执行创建市价单，如果市价单抛出异常，我就捕获异常 跳出本次异常，继续循环，知道条件条件满足
                        try:
                            print(await poloniex.create_order(symbol='BZ/USDT', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=USDT_bid_DATA-0.0001))
                        except Exception:
                            continue
                        else:
                            print(await poloniex.create_order(symbol='BZ/USDT', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices2))
                            print(await poloniex.create_order(symbol='BZ/USDT', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices3))
                            print(await poloniex.create_order(symbol='BZ/USDT', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices4))
                            print(await poloniex.create_order(symbol='BZ/USDT', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices5))
                            print(await poloniex.create_order(symbol='BZ/USDT', side='sell', type='limt', amount=Number_market_USDT_BID_BZ_UNIFORM_ETH_SELL, price=Second_building_prices6))
                            continue
        loop=asyncio.get_event_loop()
        loop.run_until_complete(print_poloniex_ethbtc_ticker())
        loop.close()
    except Exception :
    #不论订单是否成功，我都要执行撤掉订单命令
        try:
            time.sleep(60)
            list1 = []
            open_oders = exchange.fetch_open_orders(symbol='BZ/USDT')
            for order in open_oders:
                list1.append(order['id'])
            for cancel_id in list1:
                print(exchange.cancel_order(symbol='BZ/USDT', id=cancel_id))
        except Exception:
            print('清空1')
        try:
            time.sleep(5)
            list2 = []
            open_oders1 = exchange.fetch_open_orders(symbol='BZ/ETH')
            for order1 in open_oders1:
                list2.append(order1['id'])
            for cancel_id in list2:
                print(exchange.cancel_order(symbol='BZ/ETH', id=cancel_id))
        except Exception:
            print('清空2')
    # logging.debug('run')
    continue





