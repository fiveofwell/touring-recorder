from fastapi import FastAPI, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import Session

from db import create_db_and_tables, get_session
from routers.public_api_router import router as public_api_router
from routers.internal_api_router import router as internal_api_router
import security
from exceptions import TourNotFound
from security import verify_api_key, get_current_username
from schemas.api_schema import User, UserResponse

app = FastAPI(
    docs_url="/api/internal/docs",
    redoc_url="/api/internal/redoc",
    openapi_url="/api/internal/openapi.json"
)

app.include_router(public_api_router, dependencies=[Depends(verify_api_key)])
app.include_router(internal_api_router)

@app.exception_handler(TourNotFound)
async def tour_not_found_handler(
        request: Request,
        exc: TourNotFound 
):
    return JSONResponse(
        status_code=404,
        content={"detail": "Tour not found"}
    )


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return security.login(form_data.username, form_data.password, session)


@app.get("/users/me/")
def read_users_me(
    current_user_name = Depends(get_current_username)
) -> UserResponse:
    return current_user_name
