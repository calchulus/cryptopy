
from time import sleep
import argparse
from collections import OrderedDict
import time, json, ast, requests, sys, csv, math
import numpy as np
from datetime import datetime
import pandas as pd



def info():
    url = "https://www.cryptocompare.com/api/data/coinlist/"
    r = requests.get(url).json()['Data']
    coins_list = list(r.keys())
    name_list = []
    algos = {}
    proofs = {}
    for each in coins_list:
        coins_dict = r[each]
        name_list.append(coins_dict['CoinName'])
        if coins_dict['Algorithm'] not in algos:
            algos[coins_dict['Algorithm']] = 1
        else:
            algos[coins_dict['Algorithm']] += 1
        if coins_dict['ProofType'] not in proofs:
            proofs[coins_dict['ProofType']] = 1
        else:
            proofs[coins_dict['ProofType']] += 1

    return coins_list, name_list, algos, proofs
    # return coins_list

def proofs(threshold):
    allproofs = info()[3]
    popular_proofs = []
    d = {}
    for each in list(allproofs.keys()):
        if allproofs[each] > threshold:
            popular_proofs.append(each)
            d[each] = allproofs[each]
    return d

def algos(threshold):
    allalgos = info()[2]
    popular_algos = []
    d = {}
    for each in list(allalgos.keys()):
        if allalgos[each] > threshold:
            popular_algos.append(each)
            d[each] = allalgos[each]
    return d


def percentages(funct_name):





def coinusd(a):
    # input symbol
    url = "https://min-api.cryptocompare.com/data/histohour?fsym=" + (
        a + "&tsym=USD&limit=500&aggregate=1&e=CCCAGG")
    r = requests.get(url).json()['Data']
    prev_close = 0
    delta = 0
    change = 0
    times_list = [] * 24
    for i in range(len(r)):
        for j in range(24):
            hour_sec = r[i]['time']%86400
            t = int(hour_sec/3600)
            if i != 0:
                delta = (r[i]['close']-prev_close)/prev_close
                change = round(delta,5)
            if t == j:
                times_list[j].append(change)
            prev_close = r[i]['close']
    return times_list
    # for times in times_list:
    #     mean = np.mean(times)
    #     max = np.max(times)
    #     minimum = np.min(times)
    #     stand_dev = np.std(times)
    #     neg_count = 0
    #     for each in times:
    #         if each < 0:
    #             neg_count += 1
    #     results_list.append([mean,max,minimum,stand_dev,neg_count])
    # return results_list
