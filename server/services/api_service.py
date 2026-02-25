from typing import List
from sqlmodel import Session
from datetime import datetime, timezone

from models.api_model import PointInDB, TourInDB
from schemas.api_schema import Point, PointsResponse, PointsPost, TourResponse
from services.exceptions import TourNotFound
from repositories import api_repository

def get_points(tour_id: str, session: Session) -> PointsResponse:
    tour_in_db = api_repository.get_tour(tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    points_in_db = api_repository.get_points(tour_id, session)
    return PointsResponse(
            device_id = tour_in_db.device_id,
            points = [Point.model_validate(e) for e in points_in_db]
    )


def save_points(
    tour_id: str,
    points: PointsPost, 
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
            last_seen_at = now
        )
        api_repository.add_tour(tour_in_db, session)
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


def delete_tour(tour_id: str, session: Session) -> None:
    if api_repository.get_tour(tour_id, session) is None:
        raise TourNotFound()

    api_repository.delete_points(tour_id, session)
    api_repository.delete_tour(tour_id, session)

    session.commit()
    return None


def get_tours(session: Session) -> List[TourResponse]:
    return [TourResponse.model_validate(e) for e in api_repository.get_tours(session)]


def update_tour_name(
    tour_id: str,
    tour_name: str,
    session: Session
) -> TourResponse:
    tour_in_db = api_repository.get_tour(tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    tour_in_db.tour_name = tour_name
    session.commit()
    return TourResponse.model_validate(tour_in_db)
