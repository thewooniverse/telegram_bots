import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import telebot
import yfinance as yf
from dotenv import load_dotenv
import random


# random_tickers = ['COIN', 'TSLA', 'GS', 'GM', "GME", 'AAPL']
# random_prices = ['325', '1259', '12', '5', '1235', '543']


# for idx, ticker in enumerate(random_tickers):
#     output_str = f'PRICES FOR {ticker}\n'
#     output_str += f"${ticker:<15}|{'$'+random_prices[random.randint(0, len(random_prices)-1)]:>15}"
#     print(output_str)



data_5m_1m = yf.download(tickers='gme', period='5m', interval='1m')
print(data_5m_1m)

ticker = yf.Ticker('GME')
print(ticker.info)





# Langchain and OpenAI Tests

# string formatting tests

# numbers = [1235, 124123, 1250, 10, 1250]
# numbers_2 = [1259, 12, 125159, 1240, 1951]

# newples = []
# for idx in list(range(len(numbers))):
#     newples.append((numbers[idx], numbers_2[idx]))

# for n1, n2 in newples:
#     string = f"""
# Profit ${n1:<15}| {'$' + str(n1):>15}
# Delta ${n2:<15} | {n2:>15}
# """
#     print(string)



