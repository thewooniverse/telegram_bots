import os
import re
import telebot
import yfinance as yf
from dotenv import load_dotenv


"""
Practice with the following features:
- Swearword filter
-- saving the swearwords into logs with information about the sender and formatted time using dataframes to csv
-- warning system with user.id chat violations

- reading from the swearwords and other locally saved files
- sending images saved as responses

- Content type filter -> filter if the message type is this or that
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



### COMMANDS ###
@bot.message_handler(commands=['start', 'menu'])
def greet(message):
    bot.reply_to(message, "Howdy, how goes it?") # sends message in reply to the command message?





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






