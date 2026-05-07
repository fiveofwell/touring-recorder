from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.api_schema import PointsResponse, PointsPost, SavePointsResult, TourResponse, TourUpdate, User, UserResponse, DeviceResponse, DeviceFirstResponse, DevicePost
from db import get_session
from services import api_service
from security import get_current_user
from rate_limit import rate_limit

router = APIRouter(
    prefix="/api/internal",
    tags=["internal api"],
    dependencies=[Depends(rate_limit(limit=100, window=60))]
)

@router.get("/tours/{client_tour_id}/points", response_model=PointsResponse)
def get_points(
    client_tour_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return api_service.get_points(client_tour_id, current_user.id, session)


@router.post("/tours/{client_tour_id}/points", response_model=SavePointsResult)
def save_points(
    client_tour_id: str,
    points: PointsPost,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # ダミー登録なのでdevice_idはNone
    api_service.save_points(client_tour_id, points, None, current_user.id, session)
    return SavePointsResult(ok=True)


@router.delete("/tours/{client_tour_id}", status_code=204)
def delete_tour(
    client_tour_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    api_service.delete_tour(client_tour_id, current_user.id, session)
    return None


@router.get("/tours", response_model=List[TourResponse])
def get_tours(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return api_service.get_tours(current_user.id, session)


@router.patch("/tours/{client_tour_id}", response_model=TourResponse)
def update_tour_name(
    client_tour_id: str,
    body: TourUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return api_service.update_tour_name(client_tour_id, body.tour_name, current_user.id, session)


@router.get("/users/me", response_model=UserResponse)
def read_users_me(
    current_user = Depends(get_current_user)
):
    return UserResponse(username=current_user.username)


@router.get("/devices", response_model=List[DeviceResponse])
def get_devices(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return api_service.get_devices(current_user.id, session)


@router.post("/devices", response_model=DeviceFirstResponse)
def register_device(
    body: DevicePost,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return api_service.register_device(body.device_name, current_user.id, session)


@router.delete("/devices/{device_id}", status_code=204)
def delete_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    api_service.delete_device(device_id, current_user.id, session)
    return None
