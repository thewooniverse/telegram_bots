import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import telebot
import yfinance as yf
from dotenv import load_dotenv
import random

"""
Practice with the following features:

Feature: /ps [ticker] API call for yahoo finance prices for [ticker] last 5 mins of ticker
- simple usage of /ps will bring the last 5 mins of prices by default
- it should have sentiment based emoji based on the % change in the text string (practicing UTF / encoding and emojis as well)
- very similar to existing price bots on Telegram


Feature: /pc [ticker] API call for coingecko / cmc for the prices (similar to other price bots)

Feature: some kind of dialogue where the response leads to xyz, asking the user a question, and then getting some kind of response.

Feature: /chart_stock [ticker] [timefrmae]

Feature: /chart_coin [ticker] [timeframe]

Feature: /noise [ticker] -> noise level analysis along with sentiment analysis

Feature: settings - change timeframe of default images (currently, defautl settings) -> this brings us to making config files / settings files as well.
-- for each chatid, theres a directory that saves the config files for that chat (and thereby stores the logs for that chat, warning logs and configurations)

Feature: filter (delete) swearwords, warn users and mute in case of multiple violations
-- when the filter catches a bad word, it deletes the message and warns the user with the count of violations and how many strikes they have left.
--- the filter reads from a predefined list of regex / swearwords
-- a file to keep track of all of the violations thus far and check against, likely username and number of violations kept track and potentailly even the 
cell containing specifically the string that they violated with or were reported for.
-- in the case of multiple violations, they are muted to a progressive degree.

Feature: filter for content type
-- Not allowing links to be sent, potentially based on how long they've joined for. No links or no images etc...

NOTE:
Reaistically though, its not necessary for a single price bot to have all of these moderator tools as well...
Frankenstein bot almost this is... after it I am going to probably need to divide up and clean up the code a lot.

TODO:
"""


### LOADING TOKENS AND CREATING BOT ###

# loading the environment variables
load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')
OPEN_API_KEY = os.getenv('OPEN_AI_API_KEY')
# print(OPEN_API_KEY) # prints 'test ABC' correctly
# print(TG_API_KEY)

bot = telebot.TeleBot(TG_API_KEY)




### LOADING NECESSARY FILES, CONFIGS AND SETTINGS ###
# construct the dataframe with the columns -> to later add rows to, and then append to the csv file as well.




### HELPER FUNCTIONS ###
def sentiment_emoji(pct_change):
   """
   return a emoji that is ready to be sent as a string in response to mangitude of positive or negative percent that is passed.
   """
   emoji_dict = {
      "insanely_bullish": ['🌝','👽'], #90%+ above mega pumps
      "very_bullish": ['🚀', '⏫'], # 30-90% gain
      "bullish": ['📈', '🔼'], # 10-30% gain
      "slightly_bullish": ['🫰','🫶'], # 1-10% gain
      "slightly_bearish": ['😬','😐'], # 1- 10% drop 
      "bearish": ['😰', '😨'], # 10-30% drop
      "very_bearish": ['😩', '🥶'], # 30-75-% drop
      "insanely_bearish": ['🤡', '☠️', '🪦', '🤣'] # gg, -75% or higher
   }
   if pct_change >= 90:
      return random.choice(emoji_dict['insanely_bullish'])
   elif pct_change >= 30:
      return random.choice(emoji_dict['very_bullish'])
   elif pct_change >= 10:
      return random.choice(emoji_dict['bullish'])
   elif pct_change >= 0:
      return random.choice(emoji_dict['slightly_bullish'])
   elif pct_change >= -10:
      return random.choice(emoji_dict['slightly_bearish'])
   elif pct_change >= -30:
      return random.choice(emoji_dict['bearish'])
   elif pct_change >= -75:
      return random.choice(emoji_dict['very_bearish'])
   elif pct_change < -75:
      return random.choice(emoji_dict['insanely_bearish'])




def parse_big_num(number):
   """
   parses a big number like 15486874 into 15M or B or etc... based on their length and returns it in strings like
   15M, 8B, 1M, 500K etc...
   the number is positive only
   """
   categories = [(9, 'B 🐋'),
                 (6, 'M 🐬'),
                 (3, 'K 🐟')] # for anything less than 3 digits len(number)
   digits = len(str(number))

   for threshold, word in categories:
      if digits > threshold:
         cutoff_digit = int(str(number)[0:digits-threshold]) # pre-rounding
         # handle rounding
         cutoff_plus1_digit = str(number)[0:digits-threshold+1]
         last_digit_plus1 = int(cutoff_plus1_digit[-1])
         if last_digit_plus1 >= 5:
            cutoff_digit += 1

         #return with rounding
         return f'{cutoff_digit}{word}'
   return f'{str(number)}🦐'
# print(parse_big_num(1590555))
   

def pct_change(price1, price2):
   """
   Returns a % of price change of the two prices passed.
   price1 should be the first price, price 2 should be the last price
   """
#    print(f"original price {price1}")
#    print(f"final price {price2}, diff is {price1 - price2}")
   return round((((price2 - price1) / price1) * 100),2)


def is_index_stock(ticker):
   stockindex_format = f"^{ticker}"
   data = yf.download(tickers=stockindex_format, period='24h', interval='1h')
   if data.size > 0:
      return stockindex_format
   else:
      return ticker # if there is no data, then the ticker will remain the same


### COMMANDS ###
@bot.message_handler(commands=['start', 'menu'])
def greet(message):
    bot.reply_to(message, "Howdy, how goes it?") # sends message in reply to the command message?





# sample_data = yf.download(tickers='SU.TO', period='1mo', interval='1d')
# print(sample_data)

@bot.message_handler(commands=['ps'])
def send_price(message):
  """
  /ps [ticker]

  sends a message in reply to the command by the user of the last few days of recent price changes.
  example: /ps gme
  << default CHART >>
  | $GME     |    $12
  | H|L: $12 | $11
  | 24H: -5% [emoji]
  | 7d:  -5% [emoji]
  | Volume(7d): 35M
  Shill link with URL / link
  """
  # get and filter the ticker symbol from message
  request = message.text.split()[1]
  request = is_index_stock(request)

  # download all of the relevant dataframes
  ## variable names are in the format of data_timeframe_interval
  data_5m_1m = yf.download(tickers=request, period='5m', interval='1m')
  data_24h_1h = yf.download(tickers=request, period='24h', interval='1h')
  data_5d_1d = yf.download(tickers=request, period='5d', interval='1d')

  if data_5m_1m.size > 0: # some data is received, one is enough since if one works the rest will likely work, and the check is mostly for ticker validity
    # process the data into relevant columns for processing
    data_5m_1m_close = data_5m_1m['Close'].round(2)
    data_24h_1h_close = data_24h_1h['Close'].round(2)
    data_5d_1d_close = data_5d_1d['Close'].round(2)

    # get relevant prices data
    last_known_price = data_5m_1m_close.iloc[-1] 
    data_24_high = data_24h_1h_close.max()
    data_24_low = data_24h_1h_close.min()

    # get the relevant pct changes which is (first price - last price / first price) for each timeframe
    change_24h = pct_change(data_24h_1h_close.iloc[0], data_24h_1h_close.iloc[-1])
    change_7d = pct_change(data_5d_1d_close.iloc[0], data_5d_1d_close.iloc[-1])
    volume_7d = data_5d_1d['Volume'].sum()

    # process the data to plot out the image, save the image and load the image into a photo variable that can be sent with a caption.
    data_5d_1d_close.plot(kind='line', title=f'7D price for {request.upper()}')
    figure_path = f'{os.getcwd()}{os.path.sep}{request}_temp.png'
    plt.savefig(figure_path)

    # construct the string with processed data and image and send
    # construct response line by line.
    response = f"""
| ${request.upper():<10}|{last_known_price:>10}
| H|L: {data_24_high:<10}|{data_24_low:>10}
| 24H: {change_24h:>5}% {sentiment_emoji(change_24h)}
| 7d:  {change_7d:>5}% {sentiment_emoji(change_7d)}
| Vol(7d): {parse_big_num(volume_7d)}
---
<a href='https://www.example.com'>Advertise with us</a>"""


    ## read the byte and load the image and hyperlink for ref links
    with open(figure_path, 'rb') as photo:
       bot.send_photo(message.chat.id, photo, caption=response, parse_mode='HTML')

    # delete and tidy up the files / folders created
    if os.path.exists(figure_path):
       os.remove(figure_path)
    plt.clf() # clears the plots plotted so far

  else:
    bot.send_message(message.chat.id, "No data!\n For indexes please add a ^ to the ticker like ^SPX ^DJI. \nFor overseas stocks please define their market like SU.TO or WEED.TO")



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




"""
GPT feedback on sentiment_emoji:
import random

def sentiment_emoji(pct_change):
   "
   Return an emoji based on the magnitude of positive or negative percent change passed.
   "
   # Define the categories, thresholds, and corresponding emojis
   categories = [
      (90, 'insanely_bullish'),
      (30, 'very_bullish'),
      (10, 'bullish'),
      (0, 'slightly_bullish'),
      (-10, 'slightly_bearish'),
      (-30, 'bearish'),
      (-75, 'very_bearish'),
      (-float('inf'), 'insanely_bearish')  # this captures anything less than -75
   ]
   
   emoji_dict = {
      "insanely_bullish": ['🌝','👽'],
      "very_bullish": ['🚀', '⏫'],
      "bullish": ['📈', '🔼'],
      "slightly_bullish": ['🫰','🫶'],
      "slightly_bearish": ['😬','😐'],
      "bearish": ['😰', '😨'],
      "very_bearish": ['😩', '🥶'],
      "insanely_bearish": ['🤡', '☠️', '🪦', '🤣']
   }

   for threshold, sentiment in categories:
      if pct_change >= threshold:
         return random.choice(emoji_dict[sentiment])

"""


""" FEEDBACK ON Parsing big number
Your code seems to be working in the intended direction. Here's a bit of feedback and a revised version of the function:

1. **Documentation**: Your docstring is great as it provides a clear explanation of what the function does. Always maintain this practice!

2. **Using float**: If a number is `15486874`, the function would return `15M`, which is a rounded-down version. However, if you wish to provide more precision, consider formatting with float (like `15.4M`).

3. **Edge Cases**: Consider handling cases where `number` might be negative or a floating-point number.

4. **Readability**: Breaking the code into more descriptive variable names might increase the readability.

Here's a slightly modified version with more precision and handling for edge cases:

```python
def parse_big_num(number):
    "
    Parses a big number like 15486874 into 15M or B or etc... based on their length 
    and returns it in strings like 15M, 8B, 1M, 500K etc...
    "
    if not isinstance(number, (int, float)):
        return None  # or raise an appropriate error
    
    # Handle negative numbers
    sign = "-" if number < 0 else ""
    number = abs(number)
    
    categories = [(1_000_000_000, 'B'),
                  (1_000_000, 'M'),
                  (1_000, 'K')]
    
    for threshold, word in categories:
        if number >= threshold:
            return f"{sign}{number / threshold:.1f} {word}"
    return f"{sign}{number}"
```

In the above code:

- The function checks if the provided `number` is an integer or float, otherwise returns `None`.
- It handles negative numbers by extracting the sign and working with the absolute value.
- It uses actual number thresholds (like `1_000_000_000` for billion) rather than the number of digits. This makes it more explicit.
- The function returns the number with one decimal point for clarity (like `15.4M`).

Note: The usage of underscores in numbers (like `1_000_000_000`) is just for readability and is a feature available in Python 3.6 and later.
"""



