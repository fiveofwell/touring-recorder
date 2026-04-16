from fastapi import APIRouter, Depends
from sqlmodel import Session

from schemas.api_schema import PointsPost, SavePointsResult, APIKeyData
from db import get_session
from services import api_service
from security import authenticate_api_key

router = APIRouter(prefix="/api/public", tags=["public api"])

@router.post("/tours/{client_tour_id}/points", response_model=SavePointsResult)
def save_points(
    client_tour_id: str,
    points: PointsPost,
    api_key_data: APIKeyData = Depends(authenticate_api_key),
    session: Session = Depends(get_session)
):
    api_service.save_points(client_tour_id, points, api_key_data.device_id, api_key_data.user_id, session)
    return SavePointsResult(ok=True)


