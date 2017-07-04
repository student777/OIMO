import urllib.request
import json
import pprint
from utils import get_info, currency_name, currency_info


service_info = {'a': "마지막 거래 정보", 'b': '판매/구매 등록 대기 또는 거래중 내역 정보', 'c': '거래 체결 완료 내역'}
service_name = {'a': 'ticker', 'b': 'orderbook', 'c': 'recent_transactions'}

if __name__ == "__main__":

    key1 = get_info('다음 서비스 중 하나를 고르세요', service_info)
    key2 = get_info('가상화폐 종류를 고르세요', currency_info)
    url = 'https://api.bithumb.com/public/{}/{}'.format(service_name[key1], currency_name[key2])

    with urllib.request.urlopen(url) as response:
        response_dict = json.loads(response.read())
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(response_dict)
