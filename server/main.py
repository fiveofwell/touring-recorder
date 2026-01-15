from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from security import verify_api_key

from services.exceptions import TourNotFound
from db import create_db_and_tables
from routers.public_api_router import router as public_api_router
from routers.internal_api_router import router as internal_api_router
import settings

app = FastAPI()
app.include_router(public_api_router, dependencies=[Depends(verify_api_key)])
app.include_router(internal_api_router)

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
