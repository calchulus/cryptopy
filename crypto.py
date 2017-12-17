import gdax, time, json, ast, requests, sys, csv
import numpy as np
from datetime import datetime
import pandas as pd


full_list = ["bitcoin", "bitcoin_cash", "bitconnect", "dash", "ethereum_classic", "ethereum", "iota", "litecoin", "monero", "nem", "neo", "numeraire", "omisego", "qtum", "ripple", "stratis", "waves"]

def cmc(symbol):
    # takes in symbol in quotes and returns the correct thing
    #pulling from coinmarketcap datatbase

    r = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=100")

    top100 = r.json()
    # top 100 coin dictionaries


    #prints #1 coin which is currently bitcoin
    for i in range(len(top100)):
        if top100[i]['symbol'] == symbol:
            coin_index = i 
    print(top100[coin_index])


# class 

def historical(name):
    filepath = "coins/" + name + "_price.csv"
    df = pd.read_csv(filepath)
    price_list = []
    returns_list = []
    recent_close = df["Close"][0]
    ipo = df["Open"][len(df)-1]
    for price in df["Close"]:
        price_list.append(price)
    for i in range(len(price_list) -1):
        daily_return = price_list[i]/price_list[i+1] - 1 
        returns_list.append(daily_return)
    mean = np.mean(returns_list)
    max = np.max(returns_list)
    min = np.min(returns_list)
    duration_years = len(price_list)/365
    stand_dev = np.std(returns_list)
    negative_returns = []
    for i in returns_list:
        if i < 0:
            negative_returns.append(i)
    neg_mean = np.mean(negative_returns)
    sortino_sd = np.std(negative_returns)
    total_return = recent_close/ipo
    ann_return = total_return **(1/duration_years) -1
    # sharpe = (ann_return - 0.0236)/stand_dev
    # sortino = (ann_return - 0.0236)/sortino_sd
    # return sharpe, sortino
    return returns_list

    # return mean, max, min, duration_years

    # data_list = []
    # with open(filepath) as f:
    #     reader = csv.reader(f)
    #     header = next(reader)
    #     for row in reader:
    #         trip = self.read_single_trip(row)
    #         data_list.append(trip)

    # return data_list

def gains_only(name):
    returns_list = historical(name)
    positive_list = []
    for change in returns_list:
        if change > 0:
            positive_list.append(change)
    percentage = 1
    for i in positive_list:
        percentage *= (1+i)
    return percentage

def loss_only(name):
    returns_list = historical(name)
    positive_list = []
    for change in returns_list:
        if change < 0:
            positive_list.append(change)
    percentage = 1
    for i in positive_list:
        percentage *= (1+i)
    return 1/percentage

# def rebalance(name):
#     returns_list = historical(name)
#     daily_weight = 1
#     rebalanced_list = []
#     for i in returns_list:
#         rebalanced_outcome = daily_weight*i
#         rebalanced_list.append(rebalanced_outcome)
#         daily_weight = 1/(1+i)
#     print(rebalanced_list)
#     percentage = 1
#     for j in rebalanced_list:
#         percentage *= j
#     return percentage + 1

    #trying to measure returns

def corr(name1, name2, duration_days=99999, start_date=0):
    # takes two coins and returns correlations of the coins
    a = historical(name1)
    b = historical(name2)

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


def allcorr(namelist, duration_days=99999, start_date=0):
    # takes in list of coins of interest
    corr_dict = {}
    for i in range(len(namelist)-1):
        for j in range(i+1,len(namelist)):
            one_corr = corr(namelist[i],namelist[j],duration_days, start_date)
            corr_dict[namelist[i],namelist[j]] = one_corr
    bit_list = []
    alt_list = []
    for correls in corr_dict:
        # print(correls, corr_dict[correls])
        (coin1, coin2) = correls
        if coin1 == "bitcoin":
            bit_list.append(corr_dict[correls])
        else:
            alt_list.append(corr_dict[correls])
    list_stats = []
    for list_type in [bit_list, alt_list]:

        mean = np.mean(list_type)
        max = np.max(list_type)
        minimum = np.min(list_type)
        stand_dev = np.std(list_type)
        list_stats.append([mean,max,minimum,stand_dev])
    return list_stats






def dur_corr_log(name1, name, dur):
    a = historical(name1)
    b = historical(name2)
    time = min([len(a), len(b)])
    corr_log = []
    for i in range(time - dur):
        one_corr = corr(name1, name2, dur, i)
        print(one_corr)
        corr_log.append(one_corr)
    mean = np.mean(corr_log)
    max = np.max(corr_log)
    minimum = np.min(corr_log)
    stand_dev = np.std(corr_log)
    return mean, max, minimum, stand_dev


def xcdata(pair):
    '''
    takes in trading pair (ticker separated by hyphen)
    and returns statistics over period of trading

    '''
    public_client = gdax.PublicClient()
    prices = public_client.get_product_historic_rates(pair, granularity=60)

    time_list = []
    price_list = []
    low_list = []
    high_list = []
    open_price_list = []
    close_price_list = []
    vol_list = []

    for i in prices:
        time = i[0]
        low = i[1]
        high = i[2]
        open_price = i[3]
        close_price = i[4]
        vol = i[5]
        man_time = datetime.fromtimestamp(time).strftime("%A, %B %d, %Y %I:%M:%S")
        time_list.append(man_time)
        low_list.append(low)
        high_list.append(high)
        open_price_list.append(open_price)
        close_price_list.append(close_price)
        vol_list.append(vol_list)
    mean = np.mean(close_price_list)
    min = np.min(low_list)
    max = np.max(high_list)
    summary_stats_list = [mean, min, max, open_price_list[0], close_price_list[-1]]
    d = {}
    d["summary_stats"] = summary_stats_list
    d["closing_prices"] = close_price_list

    return d


def portfolio(coin):
    pass

def strat1(pair):
    output = xcdata(pair)
    [mean, min, max, first_open, last_close] = output["summary_stats"]
    close_price_list = output["closing_prices"]

    close_price_list_train = close_price_list[0:40]
    training_mean = np.mean(close_price_list_train)

    #buy one coin each time it's below training_mean

    expenditures = 0
    shares = 0

    for i in close_price_list:
        if i < training_mean:
            # buy the price
            expenditures -= i
            shares += 1
        if i > training_mean and shares > 0:
            expenditures += i
            shares -= 1
        profit = expenditures + shares * i
        # print(profit)
    #     print(expenditures)
    #     print(shares)
    # print(expenditures)
    # print(shares)

    # print(profit)
        
    #random strat
    profit = 0
    expenditures = 0
    shares = 0
    for i in range(len(close_price_list)):
        if i%2 == 0:
            expenditures -= close_price_list[i]
            shares += 1
        if i%4 == 0:
            expenditures += close_price_list[i]
            shares -= 1
        profit = expenditures + shares * close_price_list[i]
    return profit


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
    vix_list = vix()
    vix_list.reverse()
    x = vix_list[22:]
    y = historical(coin)
    for each in [x,y]:
        if x 
    a = [x[i] for i in x if i%7 == 0]
    b = [y[i] for i in x if i%7 == 0]

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


