from access_api import get_public
from datetime import datetime


COINS = ['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP']
service_name = 'recent_transactions'
timestamp = datetime.now().strftime('%m/%d-%H:%M')

with open('data/COINS_KRW', 'a') as f:
    price_list = []
    for currency in COINS:
        response = get_public(service_name, currency)
        last_item = response['data'][0]
        price_list.append(last_item['price'])
    f.write('{},{},{},{},{},{},{}\n'.format(timestamp, *price_list))
