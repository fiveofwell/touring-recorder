from typing import List
from fastapi import APIRouter, Header, Depends
from sqlmodel import Session

from schemas.api_schema import PointsResponse, PointsPost, SavePointsResult, TourResponse
from db import get_session
from services import api_service

router = APIRouter(prefix="/api/internal", tags=["internal api"])

@router.get("/tours/{tour_id}", response_model=PointsResponse)
def get_points(tour_id: str, session: Session = Depends(get_session)):
    return api_service.get_points(tour_id, session)


@router.post("/tours/{tour_id}", response_model=SavePointsResult)
def save_points(
    tour_id: str,
    points: PointsPost,
    session: Session = Depends(get_session)
):
    api_service.save_points(tour_id, points, session)
    return SavePointsResult(ok=True)


@router.delete("/tours/{tour_id}", status_code=204)
def delete_tour(tour_id: str, session: Session = Depends(get_session)):
    api_service.delete_tour(tour_id, session)
    return None


@router.get("/tours", response_model=List[TourResponse])
def get_tours(session: Session = Depends(get_session)):
    return api_service.get_tours(session)


