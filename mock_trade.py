from operator import itemgetter
from datetime import date, timedelta

INIT_KRW = 1000000
COINS = ['BTC', 'DASH', 'ETC', 'ETH', 'XRP']
START_DATE = date(2017, 7, 1)
END_DATE = date(2017, 7, 23)
PERIOD_DAYS = 7
TRANSACTION_RATE = 0.0015


def read_data(coin):
    filename = 'data/{}_KRW'.format(coin)
    with open(filename) as f:
        lines = f.readlines()
        return [(line.split()[0], float(line.split()[1].replace(',', ''))) for line in lines]


def get_best_coin(date, delta=PERIOD_DAYS):
    coin_list = []
    for coin in COINS:
        price_list = read_data(coin)
        for item in price_list:
            if item[0] == date.strftime('%Y-%m-%d'):
                break
        idx = price_list.index(item)
        curr_price = price_list[idx][1]
        prev_price = price_list[idx + delta][1]
        increase_rate = (curr_price - prev_price) / curr_price
        coin_list.append((coin, curr_price, increase_rate))

    # control group: buy KRW when bear market
    coin_list.append(('KRW', 1, 0))
    return max(coin_list, key=itemgetter(2))


def trade_daily(date, coin_prev, volume_prev):
    coin, price, increase_rate = get_best_coin(date)

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
            if d == date.strftime('%Y-%m-%d'):
                break
        volume = volume_prev * p * (1 - TRANSACTION_RATE)
    # 4) COIN1 -> COIN2
    elif coin_prev != coin:
        trade = '{}구매'.format(coin)
        price_list = read_data(coin_prev)
        for d, p in price_list:
            if d == date.strftime('%Y-%m-%d'):
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
