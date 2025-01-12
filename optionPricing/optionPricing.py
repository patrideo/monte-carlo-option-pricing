import numpy as np
from numba import jit
import yfinance as yf
from tabulate import tabulate
import sys
from datetime import datetime

def main():
    # Choosing stock
    ticker = input("For which stock would you like to value an option? Please input the ticker: ")
    stock = yf.Ticker(ticker)
    exp_date = datePicker(stock)
    options_date = stock.option_chain(exp_date)
    K, sigma = strikePicker(options_date)
    paths = int(input("How many paths would you like to run? "))
    r = 0.045
    S0 = get_current_price(stock)
    date2 = datetime.strptime(exp_date, '%Y-%m-%d')
    days_difference = (date2 - datetime.today()).days
    T = days_difference / 365.25
    option_value = msc(paths, S0, r, T, K, sigma)
    returnStats(S0, exp_date, K, option_value)

def datePicker(stock):
    expr_dates = stock.options
    # If issues with ticker.
    if not expr_dates:
        print(f"No options available for the stock ticker {stock.ticker}. Please check the ticker symbol and try again.")
        sys.exit()
    # Create a table with indexes 
    table_data = [[index, date] for index, date in enumerate(expr_dates)]
    # Printing the table for the user to pick a data
    headers = ["Index", "Expiration Date"]
    print(tabulate(table_data, headers, tablefmt="outline"))
    # Ask the user to pick a date
    index = int(input("Please select a date by entering its respective index: "))
    return expr_dates[index]

def get_current_price(stock):
    todayData = stock.history(period='1d')
    return todayData['Close'].iloc[0]

def strikePicker(options_date):
    while True:
        putORcall = input("Would you like to value a call or a put? C/P? ").lower()
        if putORcall in ["c", "p"]:
            break
    # Assign correct strike prices
    strikes = options_date.calls if putORcall == "c" else options_date.puts
    # Printing table of different contracts
    print(tabulate(strikes.loc[:, ['strike', 'bid', 'ask', 'volume', 'currency']], headers=['Index', 'Strike', 'Bid', 'Ask', 'Volume', 'Currency'], tablefmt="outline"))
    index = int(input("Please select a strike by entering its respective index: "))
    K = strikes.loc[index, 'strike']
    sigma = strikes.loc[index, 'impliedVolatility']
    return K, sigma

@jit(nopython=True)
def msc(p, S0, r, T, K, sigma):
    M = I = p
    dt = T / M
    S = np.zeros((M + 1, I))
    S[0] = S0
    rn = np.random.standard_normal(S.shape)
    for t in range(1, M + 1):
        S[t] = S[t - 1] * np.exp((r - sigma**2 / 2) * dt + sigma * np.sqrt(dt) * rn[t])
    return np.exp(-r * T) * np.maximum(K - S[-1], 0).mean()

# Return screen
def returnStats(S0, exp_date, K, option_value):
    print(f"The current stock price is {S0}.")
    print(f"The selected expiry date is {exp_date}.")
    print(f"The selected strike price is {K}.")
    print(f"The option is valued at ${option_value}.")

if __name__ == "__main__":
    main()
