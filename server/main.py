from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.exceptions import UnauthorizedKey, TourNotFound
from db import create_db_and_tables
import settings

from routers.api_router import router as api_router

app = FastAPI()
app.include_router(api_router)

origins = [
    settings.FRONTEND_ORIGIN,
]

headers = [
        "Content-Type",
        "Authorization",
        "X-API-KEY",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=headers,
)

@app.exception_handler(UnauthorizedKey)
async def unauthorized_key_handler(
        request: Request,
        exc: UnauthorizedKey 
):
    return JSONResponse(
        status_code=401,
            content={"detail": "unauthorized key"},
    )


@app.exception_handler(TourNotFound)
async def session_not_found_handler(
        request: Request,
        exc: TourNotFound 
):
    return JSONResponse(
        status_code=404,
            content={"detail": "Tour not found"},
    )


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Hello World"}
