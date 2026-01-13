import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN')

if API_KEY is None:
    raise RuntimeError()

