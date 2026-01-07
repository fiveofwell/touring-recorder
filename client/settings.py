import os
from dotenv import load_dotenv
load_dotenv()

# device / auth
DEVICE_ID = os.getenv('DEVICE_ID')
X_API_KEY = os.getenv('X_API_KEY')

# endpoints
API_URL = os.getenv('API_URL')
TOUR_START_URL = os.getenv('SESSION_START_URL')

# serial
SERIAL_PORT = os.getenv('SERIAL_PORT')
BAUDRATE = 115200
READ_TIMEOUT_SEC = 2

# queue / db
DBNAME = os.getenv('DBNAME')
SEND_LIMIT = 20

# timing
STORE_INTERVAL_SEC = 2
FLUSH_INTERVAL_SEC = 10
POST_TIMEOUT_SEC = 3
SESSION_RETRY_INTERVAL_SEC = 15

# flow control
MAX_FLOW_CONTROL = 8
