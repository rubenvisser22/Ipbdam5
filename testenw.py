import urllib.request
import ssl
import json
import time
import tweepy

# 27004hgbo3kl7i7mmds4po

map = [
    {"high": " high: "}
]
map2 = [
    {"open": " open: "}
]
map3 = [
    {"close": " Close: "}
]
map4 = [
    {"low": " low: "}
]


def final_render(asset_coin, value, key, asset):
    if key == 'symbol':
        asset_coin += " (" + asset[key] + ")"
    elif key == 'percent_change_24h':
        asset_coin += value + str(asset[key]) + "%"
    else:
        asset_coin += value + str(asset[key])
    return asset_coin

url = "https://api.lunarcrush.com/v2?data=assets&key=27004hgbo3kl7i7mmds4po&symbol=LTC"
assets = json.loads(urllib.request.urlopen(url).read())


def Highprice():
    for asset in assets['data']:
        asset_coin = ""
        for field in map:
            key = list(field.keys())[0]
            value = list(field.values())[0]
            asset_coin = final_render(asset_coin, value, key, asset)
        return asset_coin


def Openprice():
    for asset in assets['data']:
        asset_coin = ""
        for field in map2:
            key = list(field.keys())[0]
            value = list(field.values())[0]
            asset_coin = final_render(asset_coin, value, key, asset)
        return asset_coin


def Closeprice():
    for asset in assets['data']:
        asset_coin = ""
        for field in map3:
            key = list(field.keys())[0]
            value = list(field.values())[0]
            asset_coin = final_render(asset_coin, value, key, asset)
        return asset_coin


def Lowprice():
    for asset in assets['data']:
        asset_coin = ""
        for field in map4:
            key = list(field.keys())[0]
            value = list(field.values())[0]
            asset_coin = final_render(asset_coin, value, key, asset)
        return asset_coin


def splitfunctie(waarde):
    str(waarde)
    waarde = waarde.split(' ')
    waarde = float(waarde[2])
    return waarde


def main():
    splitfunctie(Highprice())
    splitfunctie(Openprice())
    splitfunctie(Closeprice())
    splitfunctie(Lowprice())

main()