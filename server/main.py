from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import redis

from db import create_db_and_tables, get_session
from routers.public_api_router import router as public_api_router
from routers.internal_api_router import router as internal_api_router
import security
from rate_limit import rate_limit
from schemas.api_schema import UserPost, UserResponse, Token
from redis_client import get_redis_client

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(public_api_router)
app.include_router(internal_api_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root(
    _: None = Depends(rate_limit(limit=10, window=60))
):
    return {"message": "Hello World"}


@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
    _: None = Depends(rate_limit(limit=5, window=60))
):
    return security.login(form_data.username, form_data.password, session)


@app.delete("/token", status_code=204)
def logout(
    current_user: UserResponse = Depends(security.get_current_user),
    _: None = Depends(rate_limit(limit=5, window=60)),
    token: str = Depends(security.oauth2_scheme),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    security.logout(token, redis_client)
    return None


@app.post("/users", response_model=UserResponse)
def create_user(
    new_user: UserPost,
    session: Session = Depends(get_session),
    _: None = Depends(rate_limit(limit=5, window=60))
):
    return security.create_user(new_user.username, new_user.password, session)

