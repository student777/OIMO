from operator import itemgetter
from datetime import date as Date, timedelta
import random
from render import read_data


INIT_KRW = 1000000
COINS = {'BTC': 0, 'ETH': 1, 'DASH': 2, 'LTC': 3, 'ETC': 4, 'XRP': 5}
START_DATE = Date(2017, 7, 1)
END_DATE = Date(2017, 7, 23)
PERIOD_DAYS = 7
TRANSACTION_RATE = 0.0015


def get_best_coin(date, delta=PERIOD_DAYS, get_crazy=False, get_only_ETH=False):
    price_now = read_data(date=date)[1]
    date_before = date - timedelta(delta)
    price_prev = read_data(date=date_before)[1]
    rate_list = [(coin, a, (a - b) / b) for coin, a, b in zip(COINS, price_now, price_prev)]

    # control group: buy KRW when bear market
    rate_list.append(('KRW', 1, 0))

    if get_crazy:
        return random.choice(rate_list)
    elif get_only_ETH:
        return rate_list[1]
    return max(rate_list, key=itemgetter(2))


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
        _, price_list = read_data(date=date)
        price_prev = price_list[COINS[coin_prev]]
        volume = volume_prev * price_prev * (1 - TRANSACTION_RATE)
    # 4) COIN1 -> COIN2
    elif coin_prev != coin:
        trade = '{}구매'.format(coin)
        _, price_list = read_data(date=date)
        price_prev = price_list[COINS[coin_prev]]
        price = price_list[COINS[coin]]
        krw = volume_prev * price_prev * (1 - TRANSACTION_RATE)  # sell
        volume = krw / price * (1 - TRANSACTION_RATE)  # buy

    estimated_asset = int(volume * price)
    print('{}: {}({:.1f}%↑), 자산:{:,}KRW'.format(date, trade, increase_rate * 100, estimated_asset))
    return coin, volume


if __name__ == '__main__':
    date = START_DATE
    coin = 'KRW'
    volume = INIT_KRW
    while date <= END_DATE:
        coin, volume = trade_daily(date, coin, volume)
        date += timedelta(days=1)
