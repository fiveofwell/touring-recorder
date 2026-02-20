from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from db import create_db_and_tables
from routers.public_api_router import router as public_api_router
from routers.internal_api_router import router as internal_api_router
from services.exceptions import TourNotFound
from security import verify_api_key
import settings

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
            content={"detail": "Tour not found"},
    )


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Hello World"}
