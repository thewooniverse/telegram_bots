


### quick and dirty script for testing out langchain / chatgpt logic before integration with bot GPT bot itself
"""
TODO:
- Followthrough of Techlead video 
-- integrate with the actual LLM, 3.5 boost or GPT 4.
-- Test out different file formats, taking on a single txt file, taking on multiple txt files
-- Test out saving conversations and using it as context;

-- Test out prompt engineering and decorating;

"""


import os
from dotenv import load_dotenv
import sys
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
import constants

# load environment keys
# load_dotenv()
# TG_API_KEY = os.getenv('TG_API_KEY')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = constants.APIKEY # this isn ot really a good solve


query = sys.argv[1]
loader = TextLoader(f'{os.getcwd()}{os.path.sep}data.txt')
index = VectorstoreIndexCreator().from_loaders([loader]) #analyzes and structurizes the data so you can query against it

# directory loading
# context_path = f"{os.gecwd()}{os.path.sep}data"
# loader = DirectoryLoader(context_path, glob='.txt')
# index = VectorstoreIndexCreator().from_loaders([loader])



# How to do __MAIN__ and its various usages, and use them in the script.

print(index.query(query, llm=ChatOpenAI()))




