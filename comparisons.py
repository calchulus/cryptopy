import gdax, time, json, ast, requests, sys, csv
import numpy as np
from datetime import datetime
import pandas as pd


def vix():
# all caps name# 
    filepath = "assets/VIX.csv"
    df = pd.read_csv(filepath)
    price_list = []
    returns_list = []
    recent_close = df["VIXClose"]

    ipo = df["VIXOpen"][0]
    for price in recent_close:
        price_list.append(price)
    for i in range(len(price_list) -1):
        daily_change = price_list[i]/price_list[i+1] - 1 
        returns_list.append(daily_change)
    mean = np.mean(returns_list)
    max = np.max(returns_list)
    minimum = np.min(returns_list)
    duration_years = len(price_list)/365
    stand_dev = np.std(returns_list)
    return returns_list


 def corr_vix(coin, duration_days=99999, start_date=0):
 	x = vix().reverse()[22:]
    y = historical(coin)
    a = [x[i] for i in x if i% 7 == 0]
    b = [y[i] for i in x if i% 7 == 0]

    if duration_days == 99999:
    # means that they want the full length.
    if len(a) < len(b):
        b = b[:len(a)]
    else: 
        a = a[:len(b)]
    else:
        oldest_date = start_date + duration_days
        a = a[start_date:oldest_date]
        b = b[start_date:oldest_date]
    x = np.array(a)
    y = np.array(b)

    r = np.corrcoef([x,y])
    corr = r[1,0]
    return corr
