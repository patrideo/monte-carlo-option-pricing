import numpy as np
import numba as nb
import yfinance as yf
from tabulate import tabulate 
import sys
import math
from datetime import datetime

def main():
    # Choosing stock
    global ticker
    global stock
    global options_date
    global exp_date
    global K
    ticker=input("For which stock would you like to value an option? Please input the ticker.")
    stock = yf.Ticker(ticker)
    
    exp_date=datePicker()
    options_date = stock.option_chain()
    K=strikePicker()
    optionValue=msc(int(input("How many paths would you like to run?")))
    print(optionValue)
    
def datePicker():
    global options_date
    global index
    expr_dates=stock.options
    if not expr_dates: 
    # If issues with ticker
        print(f"No options available for the stock ticker {ticker}. Please check the ticker symbol and try again.") 
        sys.exit()
    else: 
    # Create a table with indexes 
        table_data = [[index, date] for index, date in enumerate(expr_dates)]
    
    # Printing the table for the user to pick a data
    headers = ["Index", "Expiration Date"]
    print(tabulate(table_data, headers, tablefmt="outline"))

    # Ask the user to pick a date
    index=int(input("Please select a date by entering it's respective index."))
    return expr_dates[index]

    # Get options data for a specific expiration date
    
def get_current_price():
    todayData = stock.history(period='1d')
    return todayData['Close'].iloc[0]

# Deciding on a call or a put
def strikePicker():
    global strikes
    global sigma
    while True:    
        putORcall=input("Would you like to value a call or a put? C/P?").lower()
        if putORcall=="c" or putORcall=="p":
            break
    # Assign correct strike prices
    if putORcall=="c":
        strikes=options_date.calls
        sigma = options_date.calls.iloc[index]['impliedVolatility']
    else:
        strikes=options_date.puts
        sigma = options_date.puts.iloc[index]['impliedVolatility']

    
    # Printing table of different contractsz
    print(tabulate(strikes.loc[:, ['strike', 'bid', 'ask', 'volume', 'currency']], ['Index', 'Strike', 'Bid', 'Ask', 'Volume', 'Currency'], tablefmt="outline"))
    date_index=input("Please select a strike by entering it's respective index.")
    return strikes.loc[int(date_index), 'strike']

def msc(p):
    r=0.045
    S0=get_current_price()
    
    date2 = datetime.strptime(exp_date, '%Y-%m-%d')
    days_difference = (date2 - datetime.today()).days
    T = days_difference / 365.25

    M=I=p
    dt=T/M
    S=np.zeros((M+1, I))
    S[0]=S0
    rn=np.random.standard_normal(S.shape)
    for t in range(1, M+1):
        S[t]=S[t-1]*np.exp((r-sigma**2/2)*dt+sigma*math.sqrt(dt)*rn[t])
    
    return math.exp(-r*T)*np.maximum(K-S[-1], 0).mean()

msc_nb=nb.jit(msc)


main()






