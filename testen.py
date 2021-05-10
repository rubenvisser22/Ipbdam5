import plotly.graph_objects as go
from time import sleep
from time import *  # meaning from time import EVERYTHING
import pandas as pd
from datetime import datetime
import datetime
from tkinter import *
import os
import tkinter as tk
from datetime import datetime
import pymysql
from sqlalchemy import create_engine
import mysql.connector
import ccxt
import requests
import calendar
from pytz import timezone


def checkPatroon():
      print('wordt nu gecheckt op patroon\n')
      High = 100.56
      Low = 100.56
      Open = 100.56
      Close = 100.56

      minimaalHighprijs = 100.56
      minimaalLowprijs = Low * 0.995
      minimaalOpenPrijs = 100.56
      minimaalClosedPrijs = Close * 0.995
      MaxHighprijs = 100.56
      MaxLowprijs = Low * 1.005
      MaxOpenPrijs = 100.56
      MaxClosedPrijs = Close * 1.005

  # tijd in seconden van de time.sleep(x) // 3600 = 60 min

    # 1 betekent koop, 2 betekent verkoop. Voorbeeld: koop maruboza = 11, verkoop maruboza is 21

    # 1 |  White Marubozu | long signaal
      if minimaalHighprijs == Close == MaxHighprijs and minimaalOpenPrijs == Low == MaxOpenPrijs:
            print('werkt')
checkPatroon()