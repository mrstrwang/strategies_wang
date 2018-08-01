
import ccxt
import json
import pprint


bitz = ccxt.bitz()
apikey = bitz.apiKey = 'e08edbaef8fca9984a652e00386ec2e8'
secretkey = bitz.secret = 'HmctG3DcZyRONEA3d10wyPQ7LvYQbLToE1GFEh92MdvkvfHJaVk5DKgQYVgXoVe6'
# bitz.password = 'vJ1cE1fB3rB7fF2'


# print(json.dumps(bitz.fetch_order_book('BZ/USDT'),indent=True))
# print(bitz.fetch_ticker('BZ/USDT'))
# print(json.dumps(bitz.fetch_trades('BZ/USDT'),indent=True))

# print(json.dumps(bitz.fetch_balance()['info']))
# print(bitz.create_market_sell_order(symbol='BZ/USDT',amount=1.00))

# buy = bitz.create_order('BZ/USDT',type='market',side='buy',amount=1,price=0.2000)
# sell = bitz.create_order('BZ/USDT',type='limit',side='sell',amount=1,price=0.2533)

# bitz.cancel_order(id=2124579,symbol='BZ/USDT')
# a = bitz.fetch_open_orders('BZ/USDT')
# print(json.dumps(a[1]['id'],indent=True))  #获取当前委托单
# print(json.dumps(a,indent=True))  #获取当前委托单

# bitz.cancel_order(id=657088276,symbol='BZ/USDT')

orders = bitz.fetch_open_orders('BZ/USDT')
for i in range(len(orders)):
    print(i)
    # print(orders[i]['side'])
    if orders[i]['side'] == 'sale':
        sellid = orders[i]['id']
        print(sellid)
    elif orders[i]['side'] == 'buy':
        buyid = orders[i]['id']
        print(buyid)
    else:
        pass