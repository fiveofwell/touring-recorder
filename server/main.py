from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db import create_db_and_tables, get_session
from routers.public_api_router import router as public_api_router
from routers.internal_api_router import router as internal_api_router
import security
from schemas.api_schema import UserPost, UserResponse, Token

app = FastAPI(
    docs_url="/api/internal/docs",
    redoc_url="/api/internal/redoc",
    openapi_url="/api/internal/openapi.json"
)

app.include_router(public_api_router)
app.include_router(internal_api_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    return security.login(form_data.username, form_data.password, session)


@app.post("/users", response_model=UserResponse)
def create_user(
    new_user: UserPost,
    session: Session = Depends(get_session)
):
    return security.create_user(new_user.username, new_user.password, session)
