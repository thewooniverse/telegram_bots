import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import telebot
import yfinance as yf
from dotenv import load_dotenv
import random
import io
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton



"""
Practice with the following features:

Feature: /ps [ticker] API call for yahoo finance prices for [ticker] last 5 mins of ticker
- simple usage of /ps will bring the last 5 mins of prices by default
- it should have sentiment based emoji based on the % change in the text string (practicing UTF / encoding and emojis as well)
- very similar to existing price bots on Telegram
NEXT UP:
- /ps tidy up dataframes, intervals
- /ps pretty formatting for the graphs!


1. /start feature with buttons
-- /start shows the basic usage and set up
---- /ps /pc /settings /help in the usage / welcome message and overview
---- buttons direct you to help regarding specific functions (with more buttons)
---- settings button direct you to specific functions as well.

---- COMPELTED FEATURES ABOVE ----















ICE BOX:

Refactor dialogues for modularity.


/GPT [Query] -

BD for peepo bot will be very important -> Kudasai and other integrations, feedback, calls etc...
PLEASE USE OUR BOT!


UPGRADE: Introducing "threaded" polling / multithreading for bot;
bot = telebot.TeleBot(API_TOKEN, threaded=True) -> test it with time.sleep(2) and handling multiple requests to see what / how they respond to things.
or polling(threaded=True)
Multithreaded testing, multiple groupchats handling.





Feature: /gpt -> simple integration into calling GPT model with a specific message / query, and responding with the response from GPT.

Feature: /pc [ticker] API call for coingecko / cmc for the prices (similar to other price bots) -> csv or 

Feature: some kind of dialogue where the response leads to xyz, asking the user a question, and then getting some kind of response and then saving it into a config file.

Feature: /noise [ticker] -> noise level analysis along with sentiment analysis

Feature: configurations / settings - change timeframe of default images (currently, defautl settings) -> this brings us to making config files / settings files as well.
-- for each chatid (groupchat), there should be a directory for that chat, configs / settings, logs, bans etc...

Feature: filter (delete) swearwords, warn users and mute in case of multiple violations
-- when the filter catches a bad word, it deletes the message and warns the user with the count of violations and how many strikes they have left.
--- the filter reads from a predefined list of regex / swearwords
-- a file to keep track of all of the violations thus far and check against, likely username and number of violations kept track and potentailly even the 
cell containing specifically the string that they violated with or were reported for.
-- in the case of multiple violations, they are muted to a progressive degree.

Feature: filter for content type
-- Not allowing links to be sent, potentially based on how long they've joined for. No links or no images etc..





NOTE:
Reaistically though, its not necessary for a single price bot to have all of these moderator tools as well...
Frankenstein bot almost this is... after it I am going to probably need to divide up and clean up the code a lot.

TODO:
0. Formatting and padding using length of responses -> helper function to pretty-fy it
1. Optional interval dataset to handle different types / amounts of data available
2. Config and default config files
3. Refactor Different response types based on config files
-- Chart config
"""


### LOADING TOKENS AND CREATING BOT ###

# loading the environment variables
load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')
OPEN_API_KEY = os.getenv('OPEN_AI_API_KEY')
# print(OPEN_API_KEY) # prints 'test ABC' correctly
# print(TG_API_KEY)

bot = telebot.TeleBot(TG_API_KEY)




## Config Management ##
def load_config(group_id):
   """
   load_config(group_id), takes a single string as a group id
   """
   # if the filepath with the group ID does not exist, create the directory and the config file, then load the default config and save defaults 
   # to the newly created config.
   chat_path = f'{os.getcwd()}{os.path.sep}chats'
   group_path = f'{chat_path}{os.path.sep}{group_id}'
   config_path = f"{group_path}{os.path.sep}config.json"


   if not os.path.exists(config_path):
      # check if the group path itself exists, if it doesn't create it.
      if not os.path.exists(group_path):
         os.mkdir(group_path)
      
      # then open the default config, and write its content (default settings) into the config_path file
      with open(f"{chat_path}{os.path.sep}default_config.json", 'r') as rf:
         default_config = json.load(rf)
         # print(default_config)
         wf = open(config_path, 'w')
         json.dump(default_config, wf)
         wf.close()

   # load and return the configuration
   with open(config_path, 'r') as rf:
      config_dict = json.load(rf)
      return config_dict



def set_config(group_id, new_config):
   """
   group_id == chatid.
   new_config should be a dict config that has the same structure but with new settings
   """
   chat_path = f'{os.getcwd()}{os.path.sep}chats'
   group_path = f'{chat_path}{os.path.sep}{group_id}'
   config_path = f"{group_path}{os.path.sep}config.json"

   with open(config_path, 'w') as wf:
      json.dump(new_config, wf)




# state management handling and functions
def set_state(chat_id, state):
   """
   """
   state_log_path = f'{os.getcwd()}{os.path.sep}chats{os.path.sep}states.json'
   # checks if the state file exists, if it doesn't create an empty one
   if not os.path.exists(state_log_path):
      with open(state_log_path, 'w') as wf:
         json.dump({}, wf)
   
   # now that the state is created, we can access / open it.
   states = {}
   with open(state_log_path, 'r') as rf:
      states = json.load(rf)

   # access / amend the state
   states[chat_id] = state

   # overwrite the state:
   with open(state_log_path, 'w') as wf:
      json.dump(states, wf)
   

def get_state(chat_id):
   state_log_path = f'{os.getcwd()}{os.path.sep}chats{os.path.sep}states.json'
   with open(state_log_path, 'r') as rf:
      states = json.load(rf)
      return states.get(chat_id, 'main')




### HELPER FUNCTIONS ###
def advertisement():
   advertisements = [
      '👉Advertise with us👈',
      '👽Get Liquidated on ByBit👽',
      '🚀Trade on Binance🚀',
      '🦄Trade on UniBot🤖',
   ]
   return random.choice(advertisements)



def sentiment_emoji(pct_change):
   """
   return a emoji that is ready to be sent as a string in response to mangitude of positive or negative percent that is passed.
   """
   emoji_dict = {
      "insanely_bullish": ['🌝','👽'], #90%+ above mega pumps
      "very_bullish": ['🚀', '⏫', '🤩'], # 30-90% gain
      "bullish": ['📈', '🔼', '😮', '😻'], # 10-30% gain
      "slightly_bullish": ['🫰','🫶', '😏', '😼'], # 1-10% gain
      "slightly_bearish": ['😬','😐', '🫣', '😾'], # 1- 10% drop 
      "bearish": ['😰', '😨', '😰'], # 10-30% drop
      "very_bearish": ['😩', '🥶', '🙀'], # 30-75-% drop
      "insanely_bearish": ['🤡', '☠️', '🪦', '🤣', '😹', '🖕'] # gg, -75% or higher
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

   if number == 0:
      return "NA"


   categories = [(12, 'T'),
                 (9, 'B'),
                 (6, 'M'),
                 (3, 'K')] # for anything less than 3 digits len(number)
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
   return f'{str(number)}'


def pct_change(price1, price2):
   """
   Returns a % of price change of the two prices passed.
   price1 should be the first price, price 2 should be the last price
   """
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
def start(message):
   set_state(f'{message.chat.id}_{message.message_id}', 'main')
   response_string = f"""
Hello this is {bot.get_my_name().name}!

Press the "Help" button to find out more about the different commands I can run!

Press the "Settings" button to configure the bots and how different commands behave!

Any questions feel free to join our Telegram group!
"""
   # define markups / button handling
   markup = main_menu()
   bot.reply_to(message, response_string, reply_markup=markup)



def main_menu():
   markup = InlineKeyboardMarkup()
   settings_button = InlineKeyboardButton("Settings ⚙️", callback_data='start|settings')
   help_button = InlineKeyboardButton("Help ℹ️", callback_data='start|help')
   markup.row(settings_button, help_button)
   return markup

def settings_menu():
    # TODO: add more buttons / features in the future like localized currencies
    markup = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton("Go back 🔙", callback_data='start|main')
    ps_button = InlineKeyboardButton("/ps settings", callback_data='start|ps_settings')
    pc_button = InlineKeyboardButton("/pc settings", callback_data='start|pc_settings')
    markup.row(ps_button, pc_button)
    markup.row(back_button)
    return markup


def help_menu():
   markup = InlineKeyboardMarkup()
   ps_help_button = InlineKeyboardButton("/ps", callback_data='start|ps_help')
   pc_help_button = InlineKeyboardButton("/pc", callback_data='start|pc_help')
   back_button = InlineKeyboardButton("Go back 🔙", callback_data='start|main')
   markup.row(ps_help_button, pc_help_button)
   markup.row(back_button)
   return markup

def ps_options():
   markup = InlineKeyboardMarkup()
   back_button = InlineKeyboardButton("Go back 🔙", callback_data='start|settings')
   chart_settings_button = InlineKeyboardButton("Chart Settings 📈", callback_data='start|chart_settings')
   markup.row(chart_settings_button)
   markup.row(back_button)
   return markup

def stock_chart_menu():
   markup = InlineKeyboardMarkup()
   back_button = InlineKeyboardButton("Go back 🔙", callback_data='start|ps_settings')

   # period buttons
   p1y_button = InlineKeyboardButton("Period: 1 Year", callback_data='start|period_1y')
   pytd_button = InlineKeyboardButton("Period: YTD", callback_data='start|period_ytd')
   p3mo_button = InlineKeyboardButton("Period: 3 Month", callback_data='start|period_3mo')
   p1mo_button = InlineKeyboardButton("Period: 1 Month", callback_data='start|period_1mo')

   # interval buttons
   i1d_button = InlineKeyboardButton("Interval: 1 Day", callback_data='start|interval_1d')
   i1h_button = InlineKeyboardButton("Interval: 1 Hour", callback_data='start|interval_1h')
   i5m_button = InlineKeyboardButton("Interval: 5 Minutes", callback_data='start|interval_5m')

   # formatting the buttons
   markup.row(p1y_button, pytd_button)
   markup.row(p3mo_button, p1mo_button)
   markup.row(i1d_button, i1h_button, i5m_button)
   markup.row(back_button)
   return markup





@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'start')
def callback_handler(call):
   # get the current state of the chat
   message_key = f'{call.message.chat.id}_{call.message.message_id}'
   current_state = get_state(message_key)

   # main menu and states
   if current_state == 'main':
   # settings and settings sub menu / states
      if call.data == 'start|settings':
         # change the state
         set_state(message_key, 'settings_menu')
         # load the settings menu buttons
         markup = settings_menu()

         # load / construct the message based on current configurations
         ## the config is accessed based on chat.id, as the config files persist on a chat level instead of a message level
         config = load_config(call.message.chat.id)
         # unpack the configuration and create the response / settings message to user based on current configurations;
         settings_message = "Current Configuration:\n"
         for key,value in config.items():
            ignore_keys = ['group_id', 'admins', 'chart_settings']
            # pass all
            if key not in ignore_keys:
               settings_message+=f'{key}: {value}\n'

         # load and edit the message / buttons
         bot.edit_message_text(settings_message, call.message.chat.id, call.message.message_id, reply_markup=markup)

      if call.data == 'start|help':
         # change the state
         set_state(message_key, 'help_menu')
         # load the help menu buttons
         markup = help_menu()

         # construct the response message / string
         help_message = "Press on each button to view the help"

         # load and edit the message / buttons
         bot.edit_message_text(help_message, call.message.chat.id, call.message.message_id, reply_markup=markup)
      

   if current_state == 'settings_menu':
      if call.data == 'start|main':
         # set the state back to main:
         set_state(message_key, 'main')

         # load the markup buttons for main menu
         markup = main_menu()
         # construct the string for main menu
         response_string = f"""
Hello this is {bot.get_my_name().name}!

Press the "Help" button to find out more about the different commands I can run!

Press the "Settings" button to configure the bots and how different commands behave!

Any questions feel free to join our Telegram group!
"""
         # load and send the new message:
         bot.edit_message_text(response_string, call.message.chat.id, call.message.message_id, reply_markup=markup)
      


      # handle different price settings and change states accordingly
      if call.data == 'start|ps_settings':
         # set the state to ps_settings
         set_state(message_key, 'ps_options')

         # load the markup buttons for the ps settings menu
         markup = ps_options()

         # construct the response strings
         response_string = "/ps [stock] - Price of Stock command configuration:\n"
         response_string += "Current /ps configurations:\n-----\n"

         # load and display the configurations
         config = load_config(call.message.chat.id)

         # Portfolio Configuration
         response_string += 'Current Portfolio Settings:\n'
         response_string += f'{".".join(config["tracked_stocks"])}\n-----\n'

         # chart configurations
         response_string += 'Current Chart Settings:\n'
         chart_settings = config['chart_settings']
         stock_chart_settings = chart_settings['stocks']
         for key, value in stock_chart_settings.items():
            response_string += f'{key}: {value}\n'

         # construct the strings for the ps settings menu
         bot.edit_message_text(response_string, call.message.chat.id, call.message.message_id, reply_markup=markup)

      # pc feature is NOT built yet, therefore does not have any functionality, but it will be built in a similar way as the /ps features and settings
      if call.data == 'start|pc_settings':
         bot.answer_callback_query(call.id, "You chose /pc settings")
   


   # "ps_settings" was pressed, now we display / handle different buttons from the "ps_options" state
   if current_state == 'ps_options':

      # if user presses "go back" -> their callback data will be 'settings'
      if call.data == 'start|settings':
         # change the state
         set_state(message_key, 'settings_menu')
         # load the settings menu buttons
         markup = settings_menu()

         # load / construct the message based on current configurations
         ## the config is accessed based on chat.id, as the config files persist on a chat level instead of a message level
         config = load_config(call.message.chat.id)
         # unpack the configuration and create the response / settings message to user based on current configurations;
         settings_message = "Current Configuration:\n"
         for key,value in config.items():
            ignore_keys = ['group_id', 'admins', 'chart_settings']
            # pass all
            if key not in ignore_keys:
               settings_message+=f'{key}: {value}\n'

         # load and edit the message / buttons
         bot.edit_message_text(settings_message, call.message.chat.id, call.message.message_id, reply_markup=markup)

      # if the user presses 'chart settings' -> this will construct a new bunch of settings
      if call.data == 'start|chart_settings':
         # set the state
         set_state(message_key, 'stock_chart_settings')

         # load the markup
         markup = stock_chart_menu()

         # construct the response body string
         response_string = "/ps [stock] - Chart configurations and settings:\n"
         response_string+= "Period - how far back into the past your chart will go\n"
         response_string+= "Interval - the time intervals for your chart\n"

         # load and send the message:
         bot.edit_message_text(response_string, call.message.chat.id, call.message.message_id, reply_markup=markup)



   # if the "chart settings" button is pressed, we are now in "stock_chart_settings" state, handling all of its buttons and options
   # here is the screen where you are changing the different periods and interval buttons
   if current_state == 'stock_chart_settings':

      # if the user presses "go back" - the call data will be
      if call.data == 'start|ps_settings':
         # set the state to ps_settings
         set_state(message_key, 'ps_options')

         # load the markup buttons for the ps settings menu
         markup = ps_options()

         # construct the response strings
         response_string = "/ps [stock] - Price of Stock command configuration:\n"
         response_string += "Current /ps configurations:\n-----\n"

         # load and display the configurations
         config = load_config(call.message.chat.id)

         # Portfolio Configuration
         response_string += 'Current Portfolio Settings:\n'
         response_string += f'{".".join(config["tracked_stocks"])}\n-----\n'

         # chart configurations
         response_string += 'Current Chart Settings:\n'
         chart_settings = config['chart_settings']
         stock_chart_settings = chart_settings['stocks']
         for key, value in stock_chart_settings.items():
            response_string += f'{key}: {value}\n'

         # construct the strings for the ps settings menu
         bot.edit_message_text(response_string, call.message.chat.id, call.message.message_id, reply_markup=markup)


      # each handling should change the config on the chat.id config level and send a message in the chat to confirm! But the markups should remain the same..?
      if call.data == 'start|period_1y':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_period = config['chart_settings']['stocks']['period']
         new_period = '1y'

         config['chart_settings']['stocks']['period'] = new_period

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Time Period] has been changed from {old_period} to {new_period}"

         bot.send_message(call.message.chat.id, response_string)

      
      if call.data == 'start|period_ytd':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_period = config['chart_settings']['stocks']['period']
         new_period = 'ytd'

         config['chart_settings']['stocks']['period'] = new_period

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Time Period] has been changed from {old_period} to {new_period}"

         bot.send_message(call.message.chat.id, response_string)


      
      if call.data == 'start|period_3mo':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_period = config['chart_settings']['stocks']['period']
         new_period = '3mo'

         config['chart_settings']['stocks']['period'] = new_period

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Time Period] has been changed from {old_period} to {new_period}"

         bot.send_message(call.message.chat.id, response_string)


      
      if call.data == 'start|period_1mo':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_period = config['chart_settings']['stocks']['period']
         new_period = '1MO'

         config['chart_settings']['stocks']['period'] = new_period

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Time Period] has been changed from {old_period} to {new_period}"

         bot.send_message(call.message.chat.id, response_string)
      





      # handle all of the interval cahnges
      if call.data == 'start|interval_1d':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_interval = config['chart_settings']['stocks']['interval']
         new_interval = '1d'

         config['chart_settings']['stocks']['interval'] = new_interval

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Interval] has been changed from {old_interval} to {new_interval}"

         bot.send_message(call.message.chat.id, response_string)
      
      
      if call.data == 'start|interval_1h':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_interval = config['chart_settings']['stocks']['interval']
         new_interval = '1h'

         config['chart_settings']['stocks']['interval'] = new_interval

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Interval] has been changed from {old_interval} to {new_interval}"

         bot.send_message(call.message.chat.id, response_string)


      if call.data == 'start|interval_5m':
         # load the basic config first
         config = load_config(call.message.chat.id)

         # break down the config, to change the settings into the relevant configurations
         old_interval = config['chart_settings']['stocks']['interval']
         new_interval = '5m'

         config['chart_settings']['stocks']['interval'] = new_interval

         # set the new config and prepare the payload for the function
         set_config(call.message.chat.id, config)

         # now that the config has been changed, construct the string and notify the group / user of the changes:
         response_string = f"Configuration for [Interval] has been changed from {old_interval} to {new_interval}"

         bot.send_message(call.message.chat.id, response_string)




   # help menu handling
   if current_state == 'help_menu':
      if call.data == 'start|main':
         # set the state back to main:
         set_state(message_key, 'main')

         # load the markup buttons for main menu
         markup = main_menu()
         # construct the string for main menu
         response_string = f"""
Hello this is {bot.get_my_name().name}!

Press the "Help" button to find out more about the different commands I can run!

Press the "Settings" button to configure the bots and how different commands behave!

Any questions feel free to join our Telegram group!
"""
         # load and send the new message:
         bot.edit_message_text(response_string, call.message.chat.id, call.message.message_id, reply_markup=markup)
      

      # handle different help messages
      if call.data == 'start|ps_help':
         bot.answer_callback_query(call.id, "You chose /ps help")
      if call.data == 'start|pc_help':
         bot.answer_callback_query(call.id, "You chose /pc help")

































@bot.message_handler(commands=['ps'])
def send_price(message):
  """
  /ps [ticker]

  sends a message in reply to the command by the user of the last few days of recent price changes.
  Refresh Price button - refreshes the price with the most up to date data
  Chart - plots the price data based on the chart configuration and sends it to the chat
  """
  # load the configuration files:
  config = load_config(message.chat.id)

  # get and filter the ticker symbol from message
  request = message.text.split()[1]
  request = is_index_stock(request)

  ticker_data = yf.Ticker(request)
  try:
     mcap = ticker_data.info['marketCap']
  except:
     mcap = 0

  data_1month_5m = yf.download(tickers=request, period='1mo', interval='5m')
  
  # if some data is returned, we may process
  if data_1month_5m.size > 0:
     data_close = data_1month_5m['Close'].round(2)
     close_prices_24h = data_close.last('24H')

     # acquire each piece of information we're interested in
     last_known_price = data_close.iloc[-1]
     high_24h = close_prices_24h.max()
     low_24h = close_prices_24h.min()

     ## acquire the percent changes
     close_prices_1h = data_close.last('1H') #24h is already assigned
     close_prices_7d =  data_close.last('7D')

     pct_change_1h = pct_change(close_prices_1h.iloc[0], close_prices_1h.iloc[-1])
     pct_change_24h = pct_change(close_prices_24h.iloc[0], close_prices_24h.iloc[-1])
     pct_change_7d = pct_change(close_prices_7d.iloc[0], close_prices_7d.iloc[-1])

     # acquire the volume
     volume_7d = data_1month_5m['Volume'].last('7D').sum()

     # get the price of ETH
     price_eth = 1500

     # construct the string response
     response = f"<a href='https://finance.yahoo.com/quote/{request}'>{request.upper()}</a><pre> {'$'+str(last_known_price)}\n"
     response+= f"Ξ: {round((last_known_price/price_eth),8)}\n"
     response+= f"H|L: {str(high_24h)}|{str(low_24h)}\n"
     response+= f'{"1H":<5}{str(pct_change_1h)+"%":>8} {sentiment_emoji(pct_change_1h)}\n'
     response+= f'{"24H":<5}{str(pct_change_24h)+"%":>8} {sentiment_emoji(pct_change_24h)}\n'
     response+= f'{"7D":<5}{str(pct_change_7d)+"%":>8} {sentiment_emoji(pct_change_7d)}\n'
     response+= f'Market Cap: {parse_big_num(mcap)}\n'
     response+= f'Vol(7D): {parse_big_num(volume_7d)}\n'
     response+= f'-----\n</pre>'
     response+= f"<a href='https://www.example.com'>{advertisement()}</a>"

     markup = ps_markup(request)
     bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)
     
  
  else:
    bot.send_message(message.chat.id, "No data!\n For indexes please add a ^ to the ticker like ^SPX ^DJI. \nFor overseas stocks please define their market like SU.TO or WEED.TO")

def ps_markup(ticker):
   markup = InlineKeyboardMarkup()
   refresh_button = InlineKeyboardButton("Refresh 🔄", callback_data=f'ps|refresh|{ticker}')
   chart_button = InlineKeyboardButton("Chart 📈", callback_data=f'ps|chart|{ticker}')
   markup.row(refresh_button, chart_button)
   return markup



@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'ps')
def handle_ps_callback(call):
   if call.data.split("|")[1] == 'refresh':
      # refresh all the relevant data
      ticker = call.data.split("|")[2]
      ticker_data = yf.Ticker(ticker)
      try:
         mcap = ticker_data.info['marketCap']
      except:
         mcap = 0

      data_1month_5m = yf.download(tickers=ticker, period='1mo', interval='5m')
      data_close = data_1month_5m['Close'].round(2)
      close_prices_24h = data_close.last('24H')
      last_known_price = data_close.iloc[-1]
      high_24h = close_prices_24h.max()
      low_24h = close_prices_24h.min()

      close_prices_1h = data_close.last('1H') #24h is already assigned
      close_prices_7d =  data_close.last('7D')
      pct_change_1h = pct_change(close_prices_1h.iloc[0], close_prices_1h.iloc[-1])
      pct_change_24h = pct_change(close_prices_24h.iloc[0], close_prices_24h.iloc[-1])
      pct_change_7d = pct_change(close_prices_7d.iloc[0], close_prices_7d.iloc[-1])
      volume_7d = data_1month_5m['Volume'].last('7D').sum()

      # get the price of ETH
      price_eth = 1500
   
      response = f"<a href='https://finance.yahoo.com/quote/{ticker}'>{ticker.upper()}</a><pre> {'$'+str(last_known_price)}\n"
      response+= f"Ξ: {round((last_known_price/price_eth),8)}\n"
      response+= f"H|L: {str(high_24h)}|{str(low_24h)}\n"
      response+= f'{"1H":<5}{str(pct_change_1h)+"%":>8} {sentiment_emoji(pct_change_1h)}\n'
      response+= f'{"24H":<5}{str(pct_change_24h)+"%":>8} {sentiment_emoji(pct_change_24h)}\n'
      response+= f'{"7D":<5}{str(pct_change_7d)+"%":>8} {sentiment_emoji(pct_change_7d)}\n'
      response+= f'Market Cap: {parse_big_num(mcap)}\n'
      response+= f'Vol(7D): {parse_big_num(volume_7d)}\n'
      response+= f'-----\n</pre>'
      response+= f"<a href='https://www.example.com'>{advertisement()}</a>"

      # load the markup again
      markup = ps_markup(ticker)

      # send the message
      bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup, disable_web_page_preview=True, parse_mode='HTML')

   
   if call.data.split("|")[1] == 'chart':
   #   read and construct the price chart based on configuration settings
      ticker = call.data.split("|")[2]
      config = load_config(call.message.chat.id)
      cfg_period = config['chart_settings']['stocks']['period']
      cfg_interval = config['chart_settings']['stocks']['interval']
      
      plot_data = yf.download(tickers=ticker, period=cfg_period, interval=cfg_interval)['Close']

      if plot_data.size > 0:
         plot_data.plot(kind='line', title=f'{cfg_period} price for {ticker.upper()}')
         buf = io.BytesIO()
         plt.savefig(buf, format='png')
         buf.seek(0)

         bot.send_photo(call.message.chat.id, buf.read(), parse_mode='HTML')
         # clean the plts and close the buffer
         plt.clf()
         buf.close()
      else:
         bot.send_message(call.message.chat.id, "This combination of timeframes are not available, please change in /start -> settings")
















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



