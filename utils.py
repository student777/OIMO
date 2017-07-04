import math
import time
import hashlib
import hmac
import base64
import urllib.parse
from keys import secret_key


def black_box(endpoint_item_array):
    str_data = urllib.parse.urlencode(endpoint_item_array)
    mt = '%f %d' % math.modf(time.time())
    mt_array = mt.split(" ")[:2]
    nonce = mt_array[1] + mt_array[0][2:5]
    data = endpoint_item_array['endpoint'] + chr(0) + str_data + chr(0) + nonce
    utf8_data = data.encode('utf-8')
    utf8_key = secret_key.encode('utf-8')
    h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512)
    hex_output = h.hexdigest()
    utf8_hex_output = hex_output.encode('utf-8')
    api_sign = base64.b64encode(utf8_hex_output)
    utf8_api_sign = api_sign.decode('utf-8')
    return utf8_api_sign, nonce


def get_info(msg, choose_dict):
    print(msg)
    for key in choose_dict:
        print('{}) {}'.format(key, choose_dict[key]))
    ret_key = input()

    if ret_key not in choose_dict.keys():
        print('잘못된 입력입니다')
        exit()

    return ret_key


currency_info = {'a': '비트코인', 'b': '이더리움', 'c': '대시', 'd': '리플'}
currency_name = {'a': 'BTC', 'b': 'ETH', 'c': 'DASH', 'd': 'XRP'}
