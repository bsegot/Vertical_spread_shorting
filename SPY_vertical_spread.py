import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
import os
from datetime import timedelta
import scipy.stats as si
import sympy as sy
import sympy.stats as systats
import math


load = pd.read_csv("SPY.csv")
plt.plot(load['Close'])

returns = load['Close']
returns = returns[:-1].values / returns[1:] - 1
load['returns'] = returns
std_10days = load['returns'].rolling(10).std()
load['std_10days'] = std_10days


list_drop = []
for i in range(0,len(load)):
    date = pd.to_datetime(load['Date'][i])
    if(date.weekday() == 1):
        list_drop.append(i)
    if(date.weekday() == 2):
        list_drop.append(i)
    if(date.weekday() == 3):
        list_drop.append(i)
    if(date.weekday() == 5):
        list_drop.append(i)
    if(date.weekday() == 6):
        list_drop.append(i)

load = load.drop(load.index[list_drop])  
load = load.reset_index(drop=True)

list_save = []
for i in range(0,len(load)-1):
    date1 = pd.to_datetime(load['Date'][i])
    date2 = pd.to_datetime(load['Date'][i+1])
    if((date2-date1).days == 3):
        list_save.append(i)
        list_save.append(i+1)

def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

list_drop = returnNotMatches(list_save,range(0,len(load)))[1]
list_drop.extend([1,2])
load = load.drop(load.index[list_drop])  
load = load.reset_index(drop=True)



def euro_vanilla(S, K, T, r, sigma, option = 'call'):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option == 'call':
        result = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    if option == 'put':
        result = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
        
    return result


#to get the time to weekend I don't know if i should take T = 1/365 or T = 1/260, will check both. 
euro_vanilla(50, 100, (1/365), 0, sigma = 0, option = 'put')


T = 3/365

for i in range(0,len(load),2):
    
    #we get the central strike
    number_dec = float(str(load['Close'][i]-int(load['Close'][i]))[1:])
    if(number_dec > 0.5):
        closest_strike = math.ceil(load['Close'][i])
    else:
        closest_strike = int(load['Close'][i])
    
    call_strike = closest_strike + 1
    put_strike = closest_strike - 1
    
    call_value = euro_vanilla(load['Close'][i],call_strike,T,0,load['std_10days'][i] , option = 'call')
        
    print(call_value)
        
        
        



    
    