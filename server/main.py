from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from services.exceptions import UnauthorizedKey, TourNotFound
from db import create_db_and_tables

from routers.api_router import router as api_router

app = FastAPI()
app.include_router(api_router)

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
