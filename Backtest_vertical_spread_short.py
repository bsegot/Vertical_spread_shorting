import pandas as pd
from datetime import timedelta
from iexfinance import get_historical_data
import matplotlib.pyplot as plt

def strategy_y1(list_ticker,dates,friday_price,bankroll,fee):
    
#    bankroll = 100000
#    fee = 0.03
#    friday_price = 153.73
#    dates = "2018-10-04"
#    list_ticker = "FB"
    
    namefile_before = list_ticker + '-' + dates + '.csv'   #we load the file before earnig
    path_before = "C:\\Users\\Admin\\Desktop\\Github\\Option_chain_data\\" + namefile_before 
    load_before = pd.read_csv(path_before)
    
    Call_before = load_before.loc[load_before['Option Type'] == 'CALL']
    Put_before =  load_before.loc[load_before['Option Type'] == 'PUT']
    
    strike_call_before = 10000
    call_shorted_before = 0
    for i in range(0,len(Call_before)):
        if (0.09 <= Call_before['Bid'].tolist()[i] <= 0.15):
            strike_call_before = Call_before['Strike'].tolist()[i]
            call_shorted_before = Call_before['Bid'].tolist()[i]
            break
    strike_put_before = -10000
    put_shorted_before = 0
    for i in range(len(Put_before)-1,-1,-1):
        if (0.09 <= Put_before['Bid'].tolist()[i] <= 0.15):
            strike_put_before = Put_before['Strike'].tolist()[i]
            put_shorted_before = Put_before['Bid'].tolist()[i]
            break

    price_after_call = (max(0, friday_price - strike_call_before )) #fundamental value of the option on friday
    price_after_put = (max(0, strike_put_before - friday_price)) #fundamental value of the option on friday
    
    
    n_stock = weight / friday_price #number of stocks bought
    n_options = n_stock/100 #correspondant nunber of options we should buy
    
    #we decide to short the strangle
    bankroll = bankroll + ((call_shorted_before - price_after_call) + (put_shorted_before - price_after_put) -2*fee ) * 100 * n_options
    
    return bankroll
    





list_function_backtests = [strategy_y1]


list_ticker = ['NFLX','AAPL','MSFT','FB','BABA','JPM','XOM','V','BAC','WMT','NVDA','SPY']
dates = ["2018-10-04","2018-10-11","2018-10-18","2018-10-25","2018-11-01","2018-11-08","2018-11-22"]


bankroll = 100000 #the starting money of the portfolio
fee = 0.03 #the fee per trade / in + out
weight = 5000 #the weight of each position

incrment_list = []
incrment_list.append(bankroll)
for k in range(0,len(dates)):
    plots = []
    total_fees = []
 
    
    for j in range(0,len(list_ticker)):
           
        try:
               
            start_date = pd.to_datetime(dates[k]) + timedelta(days=1)
            end_date = pd.to_datetime(dates[k]) + timedelta(days=1)
            info = get_historical_data(list_ticker[j], start=start_date, end=end_date, output_format='pandas')
            friday_price = info['close'].tolist()[0]
            print(list_ticker[j])
            print(friday_price)
            bankroll = strategy_y1(list_ticker[j],dates[k],friday_price,bankroll,fee)

        except:
            pass #if there is no value pre-loaded in the dict or problem with those values
        
        
        incrment_list.append(bankroll)
            



plt.plot(incrment_list)
plt.ylabel('capital')
plt.xlabel('number of trades taken on thursday') 



