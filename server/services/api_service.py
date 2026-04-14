from typing import List
from sqlmodel import Session
from datetime import datetime, timezone

from models.api_model import PointInDB, TourInDB
from schemas.api_schema import Point, PointsResponse, PointsPost, TourResponse
from exceptions import TourNotFound, NotAuthorized
from repositories import api_repository

def get_points(
    client_tour_id: str,
    user_id: int,
    session: Session
) -> PointsResponse:
    tour_in_db = api_repository.get_tour_by_client_tour_id(client_tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    if tour_in_db.user_id != user_id:
        raise TourNotFound()

    points_in_db = api_repository.get_points(tour_in_db.id, session)
    return PointsResponse(
            device_id = tour_in_db.device_id,
            points = [Point.model_validate(e) for e in points_in_db]
    )


def save_points(
    client_tour_id: str,
    points: PointsPost, 
    device_id: int | None, # ブラウザからのダミー登録の場合はNULL
    user_id: int,
    session: Session
) -> None:
    now = datetime.now(timezone.utc)
    tour_in_db = api_repository.get_tour_by_client_tour_id(client_tour_id, session)

    if tour_in_db is None:
        tour_in_db = TourInDB(
            client_tour_id = client_tour_id,
            tour_name = client_tour_id,
            device_id = device_id,
            user_id = user_id,
            created_at = now,
            updated_at = now
        )
        api_repository.add_tour(tour_in_db, session)
        # tour_in_db.idを採番
        session.flush()

    elif tour_in_db.user_id != user_id:
        raise TourNotFound()
    elif tour_in_db.device_id is not None and device_id is None:
        # ダミーデータで既存のデータ上書きは不可
        raise NotAuthorized()
    else:
        tour_in_db.updated_at = now

    points_in_db = [
        PointInDB(
            tour_id = tour_in_db.id,
            client_point_id = point.client_point_id,
            latitude = point.latitude,
            longitude = point.longitude,
            recorded_at = point.recorded_at
        )
        for point in points.points
    ]

    api_repository.upsert_points(points_in_db, session)

    session.commit()
    return None


def delete_tour(
    client_tour_id: str,
    user_id: int,
    session: Session
) -> None:
    tour_in_db = api_repository.get_tour_by_client_tour_id(client_tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    if tour_in_db.user_id != user_id:
        raise TourNotFound()

    api_repository.delete_points(tour_in_db.id, session)
    api_repository.delete_tour(tour_in_db.id, session)

    session.commit()
    return None


def get_tours(
    user_id: int,
    session: Session
) -> List[TourResponse]:
    return [TourResponse.model_validate(e) for e in api_repository.get_tours(user_id, session)]


def update_tour_name(
    client_tour_id: str,
    tour_name: str,
    user_id: int,
    session: Session
) -> TourResponse:
    tour_in_db = api_repository.get_tour_by_client_tour_id(client_tour_id, session)
    if tour_in_db is None:
        raise TourNotFound()

    if tour_in_db.user_id != user_id:
        raise TourNotFound()

    tour_in_db.tour_name = tour_name
    session.commit()
    return TourResponse.model_validate(tour_in_db)
