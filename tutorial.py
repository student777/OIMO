import pprint
from access_api import get_private, get_public, trade

service_info = {
    'a': ('public', 'ticker', '마지막 거래 정보'),
    'b': ('public', 'orderbook', '판매/구매 등록 대기 또는 거래중 내역 정보'),
    'c': ('public', 'recent_transactions', '거래 체결 완료 내역'),
    'd': ('info', 'account', '회원 정보'),
    'e': ('info', 'balance', '회원 지갑 정보'),
    'f': ('info', 'wallet_address', '회원 입금 주소'),
    'g': ('info', 'ticker', '회원 마지막 거래 정보'),
    'h': ('trade', 'krw_deposit', '회원 KRW 입금 가상계좌 정보 요청'),
}

currency_info = {
    'a': ('BTC', '비트코인'),
    'b': ('ETH', '이더리움'),
    'c': ('DASH', '대시'),
    'd': ('XRP', '리플'),
}

if __name__ == "__main__":
    print('다음 서비스 중 하나를 고르세요')
    for key in service_info.keys():
        print('{}) {}'.format(key, service_info[key][2]))
    key1 = input()

    if key1 not in service_info.keys():
        print('잘못된 입력입니다')
        exit()

    print('가상화폐 종류를 고르세요')
    for key in currency_info.keys():
        print('{}) {}'.format(key, currency_info[key][1]))
    key2 = input()

    if key2 not in service_info.keys():
        print('잘못된 입력입니다')
        exit()

    api_type, service_name, _ = service_info[key1]
    currency = currency_info[key2][0]

    if api_type == 'public':
        response = get_public(service_name, currency)
    elif api_type == 'info':
        response = get_private(service_name, currency)
    elif api_type == 'trade':
        response = trade(service_name, currency)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)
