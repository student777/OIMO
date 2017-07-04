import urllib.request
import urllib.parse
import json
import pprint
from test_public import get_info, currency_name, currency_info
from secret_key import connect_key, secret_key


service_info = {'a': '회원 정보', 'b': '회원 지갑 정보', 'c': '회원 입금 주소', 'd': '회원 마지막 거래 정보',
                'e': '판/구매 거래 주문 등록 또는 진행 중인 거래', 'f': '회원 거래 내역', 'g': 'bithumb 회원 판/구매 체결 내역'}
service_name = {'a': 'account', 'b': 'balance', 'c': 'wallet_address', 'd': 'ticker',
                'e': 'orders', 'f': 'user_transactions', 'g': 'order_detail'}


if __name__ == "__main__":
    key1 = get_info('다음 서비스 중 하나를 고르세요', service_info)
    key2 = get_info('가상화폐 종류를 고르세요', currency_info)
    data = urllib.parse.urlencode({'apiKey': connect_key, 'secretKey': secret_key, 'currency': currency_name[key2]})
    data = data.encode('ascii')
    url = 'https://api.bithumb.com/info/{}'.format(service_name[key1])
    r = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(r) as response:
        the_page = response.read()
        print(the_page)

    response_dict = json.loads(response.read())
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_dict)
