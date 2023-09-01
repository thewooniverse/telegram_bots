import os
from dotenv import load_dotenv


# load environment keys
load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')
OPEN_API_KEY = os.getenv('OPEN_AI_API_KEY')




