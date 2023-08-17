import os
import matplotlib.pyplot as plt
import re
import telebot
import yfinance as yf
from dotenv import load_dotenv


"""
Practice with the following features:

Feature: /ps [ticker] API call for yahoo finance prices for [ticker] last 5 mins of ticker
- simple usage of /ps


Feature: /pc API [ticker] call for coingecko / cmc for the prices (similar to other price bots)


Feature: filter (delete) swearwords, warn users and mute in case of multiple violations
-- when the filter catches a bad word, it deletes the message and warns the user with the count of violations and how many strikes they have left.
--- the filter reads from a predefined list of regex / swearwords
-- a file to keep track of all of the violations thus far and check against, likely username and number of violations kept track and potentailly even the 
cell containing specifically the string that they violated with or were reported for.
-- in the case of multiple violations, they are muted to a progressive degree.


Feature: filter for content type
-- Not allowing links to be sent, potentially based on how long they've joined for. No links or no images etc...
"""


### LOADING TOKENS AND CREATING BOT ###

# loading the environment variables
load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')
OPEN_API_KEY = os.getenv('OPEN_AI_API_KEY')
# print(OPEN_API_KEY) # prints 'test ABC' correctly
# print(TG_API_KEY)

bot = telebot.TeleBot(TG_API_KEY)

### LOADING NECESSARY FILES ###
# construct the dataframe with the columns -> to later add rows to, and then append to the csv file as well.





data_5m = yf.download(tickers='gme', period='5m', interval='1m')
data_5m_mean = data_5m['Close'].mean() # type is dataframe
data_1d = yf.download(tickers='gme', period='1d', interval='1h')
data_1d_mean = data_1d['Close'].mean()
print(data_1d_mean)


data_30m = yf.download(tickers='gme', period='30m', interval='1m')
data_30m_close = data_30m['Close']

data_30m_close.plot(kind='line')
plt.show()







### COMMANDS ###
@bot.message_handler(commands=['start', 'menu'])
def greet(message):
    bot.reply_to(message, "Howdy, how goes it?") # sends message in reply to the command message?



@bot.message_handler(commands=['ps'])
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")


### FILTERS ###

# define a swear word filter
@bot.message_handler(regexp='shit')
def filter_swearing(message):
    bot.reply_to(message, "You can't be saying things like this here!!")




### begin code ###
bot.infinity_polling()












###### Old code snippets ######

# @bot.message_handler(commands=['wsb'])
# def get_stocks(message):
#   response = ""
#   stocks = ['gme', 'bbb']
#   stock_data = []

#   for stock in stocks: # loop through each stock
#     data = yf.download(tickers=stock, period='2d', interval='1d') # get the data from yf.download for each stock, each data is a python dataframe
#     data = data.reset_index() # resets the index to zero

#     response += f"-----{stock}-----\n" 
#     stock_data.append([stock]) # so it appends to the stock data like stock_data = [[stock] [stock] [stock]]
#     columns = ['stock']  # columns overwrites every time it loops for each stock such that for each stock, columns begins again as ['stock']
#     for index, row in data.iterrows():
#       stock_position = len(stock_data) - 1
#       price = round(row['Close'], 2)
#       format_date = row['Date'].strftime('%m/%d')
#       response += f"{format_date}: {price}\n"
#       stock_data[stock_position].append(price) # this results in soemthing like [[stock, price]]
#       columns.append(format_date) # this results in columns appending such that [stock, format_date]
#     # print(response) # optional print of the currently aggregated data

#   response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n" # populate the columns as the top of the message with formatting

#   for row in stock_data:
#     response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
#   response += "\nStock Data"
# #   print(response) # optional print of the current data
#   bot.send_message(message.chat.id, response)






