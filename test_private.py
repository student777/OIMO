import json
import pprint
import urllib.request
import urllib.parse
from utils import black_box, get_info, currency_name, currency_info
from keys import connect_key


service_info = {'a': '회원 정보', 'b': '회원 지갑 정보', 'c': '회원 입금 주소', 'd': '회원 마지막 거래 정보',
                'e': '판매/구매 거래 주문 등록 또는 진행 중인 거래', 'f': '회원 거래 내역', 'g': 'bithumb 회원 판매/구매 체결 내역'}
service_name = {'a': 'account', 'b': 'balance', 'c': 'wallet_address', 'd': 'ticker',
                'e': 'orders', 'f': 'user_transactions', 'g': 'order_detail'}


if __name__ == "__main__":
    key1 = get_info('다음 서비스 중 하나를 고르세요', service_info)
    key2 = get_info('가상화폐 종류를 고르세요', currency_info)
    api_url = "https://api.bithumb.com"
    endpoint = "/info/{}".format(service_name[key1])
    endpoint_item_array = {
        "endpoint": endpoint,
        "order_currency": currency_name[key2],  # ex) ETH
        "payment_currency": "KRW"
    }

    api_sign, nonce = black_box(endpoint_item_array)

    headers = {'Api-Key': connect_key, 'Api-Sign': api_sign, 'Api-Nonce': nonce}
    params = urllib.parse.urlencode(endpoint_item_array).encode('ascii')
    url = api_url + endpoint

    r = urllib.request.Request(url, data=params, method='POST', headers=headers)
    with urllib.request.urlopen(r) as response:
        response_dict = json.loads(response.read().decode('utf-8'))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(response_dict)
