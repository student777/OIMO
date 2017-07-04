import urllib.request
import json
import pprint


def get_info(msg, choose_dict):
    print(msg)
    for key in choose_dict:
        print('{}) {}'.format(key, choose_dict[key]))
    ret_key = input()

    if ret_key not in choose_dict.keys():
        print('잘못된 입력입니다')
        exit()

    return ret_key


service_info = {'a': "마지막 거래 정보", 'b': '판매/구매 등록 대기 또는 거래중 내역 정보', 'c': '거래 체결 완료 내역'}
service_name = {'a': 'ticker', 'b': 'orderbook', 'c': 'recent_transactions'}
currency_info = {'a': '비트코인', 'b': '이더리움', 'c': '대시', 'd': '리플'}
currency_name = {'a': 'BTC', 'b': 'ETH', 'c': 'DASH', 'd': 'XRP'}

if __name__ == "__main__":

    key1 = get_info('다음 서비스 중 하나를 고르세요', service_info)
    key2 = get_info('가상화폐 종류를 고르세요', currency_info)
    url = 'https://api.bithumb.com/public/{}/{}'.format(service_name[key1], currency_name[key2])

    response = urllib.request.urlopen(url)
    response_dict = json.loads(response.read())
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_dict)
