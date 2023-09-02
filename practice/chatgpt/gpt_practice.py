import os
from dotenv import load_dotenv
import sys
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
import constants

# load environment keys
# load_dotenv()
# TG_API_KEY = os.getenv('TG_API_KEY')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = constants.APIKEY




query = sys.argv[1]
loader = TextLoader(f'{os.getcwd()}{os.path.sep}data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query))



