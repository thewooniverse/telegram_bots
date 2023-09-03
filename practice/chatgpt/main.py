import telebot
import os
from dotenv import load_dotenv
import sys
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator




####################
###### set up ######
####################


# load environment keys and construct the bot;
load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY # find out what this bit of code does.

# construct the bots;
bot = telebot.TeleBot(TG_API_KEY)







##############################
###### helper functions ######
##############################

### config and state management helper functions ###

def chat_setup(chat_id):
    """
    Checks and sets up the necessary base files, default states, default configurations and directories necessary for the bot to operate;
    """
    return


def get_config(chat_id):
    """
    Gets and returns the configurations for the chat so that they may be used in different functions.
    """
    return


def set_config(chat_id, new_config):
    """
    Takes the new config, and overwrites the existing config file at chat_id's config path
    """






##############################
###### Message Handlers ######
##############################

@bot.message_handler(commands=['start', 'menu'])





