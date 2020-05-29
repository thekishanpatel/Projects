# Import Libraries
import requests; 
import numpy as np
import math; 
import scipy
import scipy.stats; 
from scipy.stats import norm
import statistics
from datetime import datetime, date
import os; 
os.chdir(r'') # where the client_id is stored
       
f = open('client_id')
cid = f.read()

def get_prices(ticker):
    global cid
    endpoint = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(ticker)
    payload = {'apikey': cid,
               'periodType': 'month',
               'period': 1,
               'frequencyType': 'daily',
               'freuency': 1}
    
    data = requests.get(url = endpoint, params = payload).json()
    return data

def get_volatility(data):
    delta = []
    for i in range(1, len(data['candles'])):
        d = (data['candles'][i]['close']/data['candles'][i-1]['close']) - 1
        delta.append(d)
    std = statistics.stdev(delta)
    w = std*math.sqrt(252)
    return w
        
def get_quote(ticker):
    global cid
    endpoint = "https://api.tdameritrade.com/v1/marketdata/{}/quotes".format(ticker)
    payload = {'apikey': cid
              }
    
    data = requests.get(url = endpoint, params = payload).json()
    return data[ticker]['lastPrice']

'''
Our Options are Going to be Out-Of-The Money, and will not be exercised in time. Thus, it is valid to treat the American Options like European Options.
'''
def price_options(ticker, strike, exp_date, spot_date = None, price = None, r = None, w = None, call = True):
    # Spot Price
    if (price == None):
        price = get_quote(ticker)
    # Spot Date
    if (spot_date == None):
        spot_date = date.today()
    # Time to Maturity
    T = exp_date - spot_date
    T = T.days/365
    # Interest Rate
    if (r == None):
        r = 0.01
    # Volatility
    if (w == None):
        prices = get_prices(ticker)
        w = get_volatility(prices)
    d1 = (np.log(price/strike) + (r + (0.5*(w**2)))*T) / (w * math.sqrt(T))
    d2 = d1 - (w*math.sqrt(T))
    
    c = (norm.cdf(d1)*price) - (norm.cdf(d2)*strike*math.exp(-r*T))
    if call:
        call = (norm.cdf(d1)*price) - (norm.cdf(d2)*strike*math.exp(-r*T))
        return call
    else:
        put = (norm.cdf(-d2)*strike*math.exp(-r*T)) - (norm.cdf(-d1)*price)
        return put
