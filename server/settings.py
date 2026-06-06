import os

ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOW_USER_REGISTRATION = os.getenv('ALLOW_USER_REGISTRATION')

required_vars = {
    'ALGORITHM': ALGORITHM,
    'ACCESS_TOKEN_EXPIRE_MINUTES': ACCESS_TOKEN_EXPIRE_MINUTES,
    'SECRET_KEY': SECRET_KEY,
    'ALLOW_USER_REGISTRATION': ALLOW_USER_REGISTRATION
}

for name, value in required_vars.items():
    if value is None:
        raise RuntimeError(f"環境変数 {name} が設定されていません")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
except ValueError:
    raise RuntimeError("環境変数 ACCESS_TOKEN_EXPIRE_MINUTES は整数でなければなりません")

ALLOW_USER_REGISTRATION = ALLOW_USER_REGISTRATION.lower() == "true"