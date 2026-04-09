from typing import List
from sqlmodel import Session
from datetime import datetime, timezone

from models.api_model import PointInDB, TourInDB
from schemas.api_schema import Point, PointsResponse, PointsPost, TourResponse
from exceptions import TourNotFound, NotAuthorized
from repositories import api_repository

def get_points(
    tour_id: str,
    user_id: int,
    session: Session
) -> PointsResponse:
    tour_in_db = api_repository.get_tour(tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    if tour_in_db.user_id != user_id:
        raise NotAuthorized()

    points_in_db = api_repository.get_points(tour_id, session)
    return PointsResponse(
            device_id = tour_in_db.device_id,
            points = [Point.model_validate(e) for e in points_in_db]
    )


def save_points(
    tour_id: str,
    points: PointsPost, 
    user_id: int,
    session: Session
) -> None:
    device_id = points.device_id
    now = datetime.now(timezone.utc)
    tour_in_db = api_repository.get_tour(tour_id, session)

    if tour_in_db is None:
        tour_in_db = TourInDB(
            tour_id = tour_id,
            tour_name = tour_id,
            device_id = device_id,
            started_at = now,
            last_seen_at = now,
            user_id = user_id
        )
        api_repository.add_tour(tour_in_db, session)
    elif tour_in_db.user_id != user_id:
        raise NotAuthorized()
    else:
        tour_in_db.last_seen_at = now

    points_in_db = [
        PointInDB(
            device_id = device_id,
            tour_id = tour_id,
            client_point_id = point.client_point_id,
            latitude = point.latitude,
            longitude = point.longitude,
            timestamp = point.timestamp
        )
        for point in points.points
    ]

    api_repository.upsert_points(points_in_db, session)

    session.commit()
    return None


def delete_tour(
    tour_id: str,
    user_id: int,
    session: Session
) -> None:
    tour_in_db = api_repository.get_tour(tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    if tour_in_db.user_id != user_id:
        raise NotAuthorized()

    api_repository.delete_points(tour_id, session)
    api_repository.delete_tour(tour_id, session)

    session.commit()
    return None


def get_tours(
    user_id: int,
    session: Session
) -> List[TourResponse]:
    return [TourResponse.model_validate(e) for e in api_repository.get_tours(user_id, session)]


def update_tour_name(
    tour_id: str,
    tour_name: str,
    user_id: int,
    session: Session
) -> TourResponse:
    tour_in_db = api_repository.get_tour(tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    if tour_in_db.user_id != user_id:
        raise NotAuthorized()

    tour_in_db.tour_name = tour_name
    session.commit()
    return TourResponse.model_validate(tour_in_db)
