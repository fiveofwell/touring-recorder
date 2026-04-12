from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.api_schema import PointsResponse, PointsPost, SavePointsResult, TourResponse, TourUpdate, User, UserResponse
from db import get_session
from services import api_service
from security import get_current_user

router = APIRouter(
    prefix="/api/internal",
    tags=["internal api"],
)

@router.get("/tours/{client_tour_id}", response_model=PointsResponse)
def get_points(
    client_tour_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return api_service.get_points(client_tour_id, current_user.id, session)


@router.post("/tours/{client_tour_id}", response_model=SavePointsResult)
def save_points(
    client_tour_id: str,
    points: PointsPost,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    api_service.save_points(client_tour_id, points, current_user.id, session)
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


@router.get("/users/me/")
def read_users_me(
    current_user = Depends(get_current_user)
) -> UserResponse:
    return UserResponse(username=current_user.username)

