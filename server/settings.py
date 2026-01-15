import os
from dotenv import load_dotenv
load_dotenv()

X_API_KEY = os.getenv('X_API_KEY')
FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN')

if X_API_KEY is None:
    raise RuntimeError()

