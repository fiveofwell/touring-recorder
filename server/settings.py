import os
from dotenv import load_dotenv

X_API_KEY = os.getenv('X_API_KEY')

if X_API_KEY is None:
    raise RuntimeError()

