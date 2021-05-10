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
import os
from csv import writer
import csv
import ccxt
import requests
import calendar
from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from HistoricalLitecoin import getData

connection = mysql.connector.connect(host='145.97.16.164',
                                     database='history_data',
                                     user='ruben',
                                     password='KlaasVaak123')
cursor = connection.cursor()


def connectToDB():
    host = "145.97.16.164"
    user = "ruben"
    passw = "KlaasVaak123"
    port = 3306
    database = 'history_data'

    mydb = create_engine('mysql+pymysql://' + user + ':' + passw +
                         '@' + host + ':' + str(port) + '/' + database, echo=False)

    if(mydb):
        print("Connectie met database gelukt!\n")
        print(mydb)
        return mydb
    else:
        print("Connectie met database is niet gelukt!\n")
        return False

def historischeData():
    
    df = pd.read_csv(
        r"C:\Users\ruben\OneDrive\Bureaublad\School huiswerk\Jaar 2\IPBDAM2\Litecoin\prijs.csv", dtype={'high': np.float64, 'low': np.float64, 'close': np.float64, 'open': np.float64})
    return df


def getCoinData(df,dbCon):  # ieder uur actuele data uploaden uploaden | deze functie in een ander python script?
    dbConnectie = dbCon
    price = df['high'] + df['low'] / 2
    litecoinDF = {
        'prijs': price,
        'Highprijs': df['high'],
        'Lowprijs': df['low'],
        'OpenPrijs': df['open'],
        'ClosedPrijs': df['close'],
        'Periode': df['time']}
    litecoinDF = pd.DataFrame(litecoinDF)
    litecoinDF.to_sql(name='prijs', con=dbConnectie,
                      if_exists='append', index=False)
    return litecoinDF


def historischeTransactie(signaal, aantalCoins, dbConn, index):
    df = historischeData()
    dbConnectie = dbConn
    iloc = df.iloc[index]
    high = iloc['high']
    low = iloc['low']
    price = high + low / 2
    date = iloc['time']
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


def checkPatroon(df, index, dbConn):
    print('wordt nu gecheckt op patroon\n')
    High = df['high']
    Low = df['low']
    Open = df['open']
    Close = df['close']
    minimaalHighprijs = High * 0.999
    minimaalLowprijs = Low * 0.999
    minimaalOpenPrijs = Open * 0.999
    minimaalClosedPrijs = Close * 0.999
    MaxHighprijs = High * 1.001
    MaxLowprijs = Low * 1.001
    MaxOpenPrijs = Open * 1.001
    MaxClosedPrijs = Close * 1.001
    
    origineleIndex = index
    toekomstigeIndex = index + 1
  # tijd in seconden van de time.sleep(x) // 3600 = 60 min

    # 1 betekent koop, 2 betekent verkoop. Voorbeeld: koop maruboza = 11, verkoop maruboza is 21

    # 1 |  White Marubozu | long signaal
    if minimaalHighprijs <= Close <= MaxHighprijs and minimaalOpenPrijs <= Low <= MaxOpenPrijs:
        
        signaal = 11
        aantalCoins = Koop(signaal, origineleIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, origineleIndex)
        signaal = 21
        aantalCoins = Verkoop(aantalCoins, toekomstigeIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, toekomstigeIndex)

    # 2 | Bearisch Gravestone Doji | short signaal
    elif minimaalOpenPrijs <= Low <= MaxOpenPrijs and minimaalOpenPrijs <= Close <= MaxOpenPrijs:

        signaal = 12
        aantalCoins = Koop(signaal, origineleIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, origineleIndex)
        signaal = 22
        aantalCoins = Verkoop(aantalCoins, toekomstigeIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, toekomstigeIndex)

    # 3 | Bullish Dragonfly Doji | long signaal
    elif minimaalOpenPrijs <= High <= MaxOpenPrijs and minimaalOpenPrijs <= Close <= MaxOpenPrijs:

        signaal = 13
        aantalCoins = Koop(signaal, origineleIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, origineleIndex)
        signaal = 23
        aantalCoins = Verkoop(aantalCoins, toekomstigeIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, toekomstigeIndex)

    # # 4 | Bearish Long Black Candle | short prijs
    elif Low < Close < Open and Open < High:

        signaal = 14
        aantalCoins = Koop(signaal, origineleIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, origineleIndex)
        signaal = 24
        aantalCoins = Verkoop(aantalCoins, toekomstigeIndex)
        historischeTransactie(signaal, aantalCoins, dbConn, toekomstigeIndex)


def Koop(signaal, index):
    df = historischeData()
    iloc = df.iloc[index]
    high = iloc['high']
    low = iloc['low']
    price = high + low / 2
    print(price)
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



def Verkoop(aantalCoins, index):
    df = historischeData()

    iloc = df.iloc[index]
    high = iloc['high']
    low = iloc['low']
    price = high + low / 2
    print(price)
    print(aantalCoins)
    saldo = (aantalCoins * price)
    print(saldo)
    print('huidge eurowaarde coins:', saldo)
    verkoopQuery = f"UPDATE gebruiker SET Saldo = Saldo + {saldo}, Positie = 'Geen' where idGebruiker = 1;"
    cursor.execute(verkoopQuery)
    connection.commit()
    print(100 - saldo, 'winst of verlies gemaakt')
    index = index + 1
    return -aantalCoins


def start():
    dbConn = connectToDB()
    df = historischeData()
    for index, row in df.iterrows():
        print('dit is index:',index)
        print('\nrow: ',row)
        getCoinData(df, dbConn)
        checkPatroon(row, index, dbConn)
        # getCoinData()
        print('row gedaan')
        # index = index + 1


def main():
    start()


if __name__ == "__main__":
    main()
