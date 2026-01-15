from typing import List
from fastapi import APIRouter, Header, Depends
from sqlmodel import Session

from schemas.api_schema import PointsResponse, PointsPost, SavePointsResult, TourResponse
from db import get_session
from services import api_service

router = APIRouter(prefix="/api/public", tags=["public api"])

@router.post("/tours/{tour_id}", response_model=SavePointsResult)
def save_points(
    tour_id: str,
    points: PointsPost,
    session: Session = Depends(get_session)
):
    api_service.save_points(tour_id, points, session)
    return SavePointsResult(ok=True)


