import math
import time
import hashlib
import hmac
import base64
import urllib.request
import json
import urllib.parse
from keys import connect_key, secret_key


def get_public(service, currency):
    url = 'https://api.bithumb.com/public/{}/{}'.format(service, currency)
    with urllib.request.urlopen(url) as response:
        response_dict = json.loads(response.read().decode('utf-8'))
        return response_dict


def get_private(service, currency, extra_params={}):
    api_url = "https://api.bithumb.com"
    endpoint = "/info/{}".format(service)
    endpoint_item_array = {
        "endpoint": endpoint,
        "currency": currency,  # ex) ETH
    }
    endpoint_item_array.update(extra_params)

    api_sign, nonce = black_box(endpoint_item_array)

    headers = {'Api-Key': connect_key, 'Api-Sign': api_sign, 'Api-Nonce': nonce}
    params = urllib.parse.urlencode(endpoint_item_array).encode('ascii')
    url = api_url + endpoint

    r = urllib.request.Request(url, data=params, method='POST', headers=headers)
    with urllib.request.urlopen(r) as response:
        response_dict = json.loads(response.read().decode('utf-8'))
        return response_dict


def trade(service, currency, extra_params={}):
    api_url = "https://api.bithumb.com"
    endpoint = "/trade/{}".format(service)
    endpoint_item_array = {
        "endpoint": endpoint,
        "currency": currency,  # ex) ETH
    }
    endpoint_item_array.update(extra_params)

    api_sign, nonce = black_box(endpoint_item_array)

    headers = {'Api-Key': connect_key, 'Api-Sign': api_sign, 'Api-Nonce': nonce}
    params = urllib.parse.urlencode(endpoint_item_array).encode('ascii')
    url = api_url + endpoint

    r = urllib.request.Request(url, data=params, method='POST', headers=headers)
    with urllib.request.urlopen(r) as response:
        response_dict = json.loads(response.read().decode('utf-8'))  # .decode(): for python 3.5
        return response_dict


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
