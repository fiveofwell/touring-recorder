from typing import List
from fastapi import APIRouter, Header
from schemas.api_schema import DataRead, DataPost, TourRead, AcceptedData
from services import api_service

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/gps/points", response_model=List[DataRead])
def get_data():
    return api_service.get_data()


@router.post("/gps/points", response_model=AcceptedData)
def save_points(data: DataPost, x_api_key: str = Header(..., alias="X-API-KEY")):
    return api_service.save_points(data.tour_id, data.points, x_api_key)


@router.get("/tours", response_model=List[TourRead])
def get_tours():
    return api_service.get_tours()


@router.get("/tours/start", response_model=TourRead)
def start_tour():
    return api_service.start_tour()


