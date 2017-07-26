from operator import itemgetter
from datetime import date, timedelta
import random
from render import read_data


INIT_KRW = 1000000
COINS = ['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP']
START_DATE = date(2017, 5, 3)
END_DATE = date(2017, 7, 23)
PERIOD_DAYS = 7
TRANSACTION_RATE = 0.0015


# FIXME
def get_best_coin(date, delta=PERIOD_DAYS, get_crazy=False, get_only_ETH=False):
    coin_list = []

    price_now = read_data(date=date.today())[1]
    date_before = date.today() - timedelta(delta)
    price_prev = read_data(date=date_before)[1]
    rate_list = [(coin, a, (a - b) / b) for coin, a, b in zip(COINS, price_now, price_prev)]

    # control group: buy KRW when bear market
    rate_list.append(('KRW', 1, 0))

    if get_crazy:
        return random.choice(rate_list)
    elif get_only_ETH:
        return rate_list[1]
    return max(rate_list, key=itemgetter(2))

# FIXME
def trade_daily(date, coin_prev, volume_prev):
    coin, price, increase_rate = get_best_coin(date)  # Modify here

    # 1) KRW -> KRW, COIN -> COIN
    if coin_prev == coin:
        trade = '{}보유'.format(coin)
        volume = volume_prev
    # 2) KRW -> COIN
    elif coin_prev == 'KRW':
        trade = '{}구매'.format(coin)
        volume = volume_prev / price * (1 - TRANSACTION_RATE)
    # 3) COIN -> KRW
    elif coin == 'KRW':
        trade = '{}판매'.format(coin_prev)
        price_list = read_data(coin_prev)
        for d, p in price_list:
            if d == date.strftime('%m/%d'):
                break
        volume = volume_prev * p * (1 - TRANSACTION_RATE)
    # 4) COIN1 -> COIN2
    elif coin_prev != coin:
        trade = '{}구매'.format(coin)
        price_list = read_data(coin_prev)
        for d, p in price_list:
            if d == date.strftime('%m/%d'):
                break
        krw = volume_prev * p * (1 - TRANSACTION_RATE)
        volume = krw / price * (1 - TRANSACTION_RATE)

    print('{}: {}({:.1f}%↑), 자산:{:.0f}KRW'.format(date, trade, increase_rate * 100, volume * price))
    return coin, volume


if __name__ == '__main__':
    assets = INIT_KRW
    date = START_DATE
    coin = 'KRW'
    volume = INIT_KRW
    while date <= END_DATE:
        coin, volume = trade_daily(date, coin, volume)
        date += timedelta(days=1)
