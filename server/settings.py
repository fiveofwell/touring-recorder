import os

X_API_KEY = os.getenv('X_API_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.getenv('SECRET_KEY')

required_vars = {
    'X_API_KEY': X_API_KEY,
    'ALGORITHM': ALGORITHM,
    'ACCESS_TOKEN_EXPIRE_MINUTES': ACCESS_TOKEN_EXPIRE_MINUTES,
    'SECRET_KEY': SECRET_KEY,
}

for name, value in required_vars.items():
    if value is None:
        raise RuntimeError(f"環境変数 {name} が設定されていません")

