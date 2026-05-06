from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from schemas.api_schema import User, UserResponse, Token, TokenData, APIKeyData
from models.api_model import UserInDB
from db import get_session
from repositories import api_repository
import settings

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

api_key_header = APIKeyHeader(name='X-API-KEY')

def unauthorized_exception(detail: str, bearer: bool = False) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"} if bearer else None,
    )


def authenticate_api_key(
        api_key: str = Depends(api_key_header),
        session: Session = Depends(get_session)
):
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    api_key_in_db = api_repository.get_api_key(key_hash, session)

    if api_key_in_db is None or api_key_in_db.disabled:
        raise unauthorized_exception(
            "Could not validate credentials"
        )

    device_in_db = api_repository.get_device(api_key_in_db.device_id, session)
    user_id = device_in_db.user_id

    api_key_in_db.last_used_at = datetime.now(timezone.utc)
    session.commit()

    return APIKeyData(
        device_id=api_key_in_db.device_id,
        user_id=user_id
    )


def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return password_hash.hash(password)


def authenticate_user(
    username: str,
    password:str,
    session: Session
):
    user = api_repository.get_user(username, session)
    if not user:
        # タイミング攻撃対策のためダミーで検証
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def login(
    username: str,
    password: str,
    session: Session
) -> Token:
    user = authenticate_user(username, password, session)
    if not user:
        raise unauthorized_exception(
            "Incorrect username or password",
            bearer=True
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    credentials_exception = unauthorized_exception(
        "Could not validate credentials",
        bearer=True
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = api_repository.get_user(token_data.username, session)
    if user is None:
        raise credentials_exception

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return User.model_validate(user)


def create_user(
    username: str,
    password: str,
    session: Session
):
    hashed_password = get_password_hash(password)
    user_in_db = UserInDB(
        username=username,
        hashed_password=hashed_password,
        disabled=False
    )
    api_repository.add_user(user_in_db, session)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    return UserResponse(username=user_in_db.username)


def generate_api_key() -> tuple[str, str, str]:
    """
    Returns:
        raw_key:    平文フルキー
        key_prefix: 一覧表示用プレフィックス
        key_hash:   DB保存用ハッシュ
    """
    raw_key = "sk-tr-" + secrets.token_urlsafe(32)
    key_prefix = raw_key[:16] + "****"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, key_prefix, key_hash
