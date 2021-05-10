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

screen = tk.Tk()
connection = mysql.connector.connect(host='145.97.16.164',
                                     database='mydb2',
                                     user='ruben',
                                     password='KlaasVaak123')
cursor = connection.cursor()

sql1 = "select saldo from gebruiker"
cursor.execute(sql1)
saldo = cursor.fetchall()

saldo = saldo[0]


def main_screen():
    global screen
    screen.geometry("300x170")
    screen.title("Saldo check")
    Label(text="Welkom Rudolf", bg="black", width="300", foreground="white",
          height="2", font=("Calibri", 13)).pack()
    Label(text="", bg="black", width="300", height="1",font=("Calibri", 13)).pack()
    Label(text="Uw saldo is:", bg="black", width="300", foreground="white",
          height="2", font=("Calibri", 13)).pack()
    Label(text=saldo, bg="black", width="300", foreground="green",
          height="2", font=("Calibri", 13)).pack()
    screen.mainloop()




main_screen()

df = pd.read_csv(
    'prijs.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                     open=df['OpenPrijs'],
                                     high=df['Highprijs'],
                                     low=df['Lowprijs'],
                                     close=df['ClosedPrijs'])])

fig.show()

