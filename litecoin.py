import ssl
import urllib.request
import pymysql
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
import numpy as np
import requests
import json
import re
import datetime
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from time import sleep
from time import *  # meaning from time import EVERYTHING
import time
import os
from csv import writer
import csv
import ccxt
import requests
import calendar
from pytz import timezone

# Class of different styles


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


connection = mysql.connector.connect(host='145.97.16.164',
                                     database='mydb2',
                                     user='ruben',
                                     password='KlaasVaak123')
cursor = connection.cursor()


def connectToDB():
    host = "145.97.16.164"
    user = "ruben"
    passw = "KlaasVaak123"
    port = 3306
    database = 'mydb2'

    mydb = create_engine('mysql+pymysql://' + user + ':' + passw +
                         '@' + host + ':' + str(port) + '/' + database, echo=False)

    if(mydb):
        print("Connectie met database gelukt!\n")
        print(mydb)
        return mydb
    else:
        print("Connectie met database is niet gelukt!\n")
        return False


def dateTimeInstall():
    amsterdam = timezone('Europe/Amsterdam')
    now = datetime.now(amsterdam)
    begin = calendar.timegm(now.utctimetuple())
    since = (begin - 120 * 60) * 1000  # UTC timestamp in milliseconds
    print('tijdzone is ingesteld\n')
    return since


def setTimeFrame(since):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(
        symbol='LTC/EUR', timeframe='1h', since=since, limit=1)
    print('ohlcv opgehaald\n')
    return ohlcv


def writeToDataframe(ohlcv):
    df = pd.DataFrame(
        ohlcv, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Time'] = [datetime.fromtimestamp(
        float(time) / 1000) for time in df['Time']]
    df.set_index('Time', inplace=True)
    print('df geinstantieerd\n')
    return df


def getPriceData():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    binance_df = pd.DataFrame(requests.get(url).json())
    litecoinDF = binance_df[binance_df["symbol"] == "LTCEUR"]
    price = litecoinDF['lastPrice']
    price = float(price)
    return price


def getCoinData(df):  # ieder uur actuele data uploaden uploaden | deze functie in een ander python script?
    dbConnectie = connectToDB()
    price = getPriceData()
    time = datetime.now(timezone('Europe/Amsterdam'))
    litecoinDF = {
        'prijs': price,
        'Highprijs': df['High'],
        'Lowprijs': df['Low'],
        'OpenPrijs': df['Open'],
        'ClosedPrijs': df['Close'],
        'Periode': time}
    litecoinDF = pd.DataFrame(litecoinDF)
    print(litecoinDF.head)
    litecoinDF.to_sql(name='prijs', con=dbConnectie,
                      if_exists='append', index=False)


def historischeTransactie(signaal, aantalCoins):
    dbConnectie = connectToDB()
    price = getPriceData()
    price = float(price)
    date = datetime.now(timezone('Europe/Amsterdam'))
    transactie_data = {
        'prijs': price,
        'periode': date,
        'aantalCoins': aantalCoins,
        'idGebruiker': 1,
        'actie': signaal
    }
    transactieDF = pd.DataFrame(transactie_data, index=[0])
    transactieDF.to_sql(name='transactie', con=dbConnectie,
                        if_exists='append', index=False)

# def schrijfnaarcsv():
#     since = dateTimeInstall()
#     ohlcv = setTimeFrame(since)
#     df = writeToDataframe(ohlcv)
#     Date = datetime.datetime.now()
#     High = float(df['High'])
#     Low = float(df['Low'])
#     Open = float(df['Open'])
#     Close = float(df['Close'])
#     with open('prijs.csv', 'a', newline='') as f:
#         List = [Date, Open, High, Lowprijs, ClosedPrijs]
#         writer = csv.writer(f)
#         writer.writerow(List)
#         f.close()


def checkPatroon(df):
    print('wordt nu gecheckt op patroon\n')
    High = float(df['High'])
    Low = float(df['Low'])
    Open = float(df['Open'])
    Close = float(df['Close'])

    minimaalHighprijs = float(High) * 0.995
    minimaalLowprijs = float(Low) * 0.995
    minimaalOpenPrijs = float(Open) * 0.995
    minimaalClosedPrijs = float(Close) * 0.995
    MaxHighprijs = float(High) * 1.005
    MaxLowprijs = float(Low) * 1.005
    MaxOpenPrijs = float(Open) * 1.005
    MaxClosedPrijs = float(Close) * 1.005

    x = 3600  # tijd in seconden van de time.sleep(x) // 3600 = 60 min

    # format long signaal transactie
    # ====================================
    # signaal = 12
    # aantalCoins = Koop(signaal)
    # print('er is gekocht met signaal:', signaal)
    # historischeTransactie(signaal, aantalCoins)
    # print('\ntransactie opgeslagen\n')
    # time.sleep(x)
    # signaal = 22
    # aantalCoins = Verkoop(aantalCoins)
    # print('er is verkocht met signaal:', signaal)
    # historischeTransactie(signaal, aantalCoins)
    # print('\ntransactie opgeslagen\n')

    # 1 betekent koop, 2 betekent verkoop. Voorbeeld: koop maruboza = 11, verkoop maruboza is 21

    # 1 |  White Marubozu | long signaal
    if minimaalHighprijs <= Close <= MaxHighprijs and minimaalOpenPrijs <= Low <= MaxOpenPrijs:

        signaal = 11
        aantalCoins = Koop(signaal)
        historischeTransactie(signaal, aantalCoins)
        time.sleep(x)
        signaal = 21
        aantalCoins = Verkoop(aantalCoins)
        historischeTransactie(signaal, aantalCoins)

    # 2 | Bearisch Gravestone Doji | short signaal
    elif minimaalOpenPrijs <= Low <= MaxOpenPrijs and minimaalOpenPrijs <= Close <= MaxOpenPrijs:

        signaal = 12
        aantalCoins = Koop(signaal)
        historischeTransactie(signaal, aantalCoins)
        time.sleep(x)
        signaal = 22
        aantalCoins = Verkoop(aantalCoins)
        historischeTransactie(signaal, aantalCoins)

    # 3 | Bullish Dragonfly Doji | long signaal
    elif minimaalOpenPrijs <= High <= MaxOpenPrijs and minimaalOpenPrijs <= Close <= MaxOpenPrijs:

        signaal = 13
        aantalCoins = Koop(signaal)
        historischeTransactie(signaal, aantalCoins)
        time.sleep(x)
        signaal = 23
        aantalCoins = Verkoop(aantalCoins)
        historischeTransactie(signaal, aantalCoins)

    # # 4 | Bearish Long Black Candle | short prijs
    elif Low < Close < Open and Open < High:

        signaal = 14
        aantalCoins = Koop(signaal)
        historischeTransactie(signaal, aantalCoins)
        time.sleep(x)
        signaal = 24
        aantalCoins = Verkoop(aantalCoins)
        historischeTransactie(signaal, aantalCoins)


def Koop(signaal):
    price = getPriceData()
    aantalCoins = 100/price

    if (signaal % 2) == 0:
        print('long gaan')
        aantalCoins = 100 / price
        koopQuery = "UPDATE gebruiker SET Saldo = Saldo - 100"
        cursor.execute(koopQuery)
        connection.commit()

    else:
        print('short gaan')
        aantalCoins = -100 / price
        koopQuery = "UPDATE gebruiker SET Saldo = Saldo + 100"
        cursor.execute(koopQuery)
        connection.commit()

    print(aantalCoins, 'litecoins gekocht')
    return aantalCoins


def Verkoop(aantalCoins):
    price = getPriceData()
    saldo = (aantalCoins * price)
    print('huidge eurowaarde coins:', saldo)
    verkoopQuery = f"UPDATE gebruiker SET Saldo = Saldo + {saldo}, Positie = 'Geen' where idGebruiker = 1;"
    cursor.execute(verkoopQuery)
    connection.commit()
    print(100 - saldo, 'winst of verlies gemaakt')
    return -aantalCoins


def start():
    dbConn = connectToDB()
    time = dateTimeInstall()
    ohlcv = setTimeFrame(time)
    df = writeToDataframe(ohlcv)
    getCoinData(df)
    checkPatroon(df)
    print('start klaar')


def main():
    sched = BlockingScheduler()
    print('schedular gestart')
    # deze scheduler moeten we uiteindelijk gaan gebruiken
    sched.add_job(start, "cron", day_of_week='mon-sun',
                  hour='9-20', minute='0', second='10')
    # sched.add_job(start, 'interval', seconds=10)
    sched.start()


if __name__ == "__main__":
    main()
