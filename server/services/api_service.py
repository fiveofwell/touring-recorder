from typing import List
from sqlmodel import Session
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import uuid

from models.api_model import PointInDB, TourInDB, DeviceInDB, APIKeyInDB
from schemas.api_schema import Point, PointsResponse, PointsPost, TourResponse, DeviceResponse, DeviceFirstResponse, APIKeyResponse
from repositories import api_repository
from security import generate_api_key

def get_points(
    client_tour_id: str,
    user_id: int,
    session: Session
) -> PointsResponse:
    tour_in_db = api_repository.get_tour_by_client_tour_id(client_tour_id, session)
    if tour_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    if tour_in_db.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )


    points_in_db = api_repository.get_points(tour_in_db.id, session)
    return PointsResponse(
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
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


def delete_tour(
    client_tour_id: str,
    user_id: int,
    session: Session
) -> None:
    tour_in_db = api_repository.get_tour_by_client_tour_id(client_tour_id, session)
    if tour_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    if tour_in_db.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    api_repository.delete_points(tour_in_db.id, session)
    api_repository.delete_tour(tour_in_db.id, session)

    session.commit()


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    if tour_in_db.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    tour_in_db.tour_name = tour_name
    session.commit()
    return TourResponse.model_validate(tour_in_db)


def get_devices(
    user_id: int,
    session: Session
) -> List[DeviceResponse]:
    return [DeviceResponse(device_id=device.device_id, device_name=device.device_name, api_key=APIKeyResponse.model_validate(api_key)) for device, api_key in api_repository.get_devices(user_id, session)]

    
def register_device(
    device_name: str,
    user_id: int,
    session: Session
) -> DeviceFirstResponse:
    device_id=str(uuid.uuid4())
    device_in_db = DeviceInDB(
        device_id=device_id,
        user_id=user_id,
        device_name=device_name
    )
    try:
        api_repository.add_device(device_in_db, session)
        # device_in_db.idを採番
        session.flush()

        raw_key, key_prefix, key_hash = generate_api_key()
        api_key_in_db = APIKeyInDB(
            device_id=device_in_db.id,
            key_hash=key_hash,
            key_prefix=key_prefix,
            created_at=datetime.now(timezone.utc)
        )
        api_repository.add_api_key(api_key_in_db, session)

        session.commit()
    except IntegrityError:
        session.rollback()
        if api_repository.get_device_by_device_name(device_in_db.device_name, user_id, session) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Device already exists"
            )
        raise

    return DeviceFirstResponse(
        device_id=device_id,
        device_name=device_name,
        api_key=raw_key
    )


def delete_device(
    device_id: str,
    user_id: int,
    session: Session
) -> None:
    device_in_db = api_repository.get_device_by_device_id(device_id, user_id, session)
    if device_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    if device_in_db.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )


    api_repository.delete_device(device_in_db.id, session)
    api_repository.delete_api_key(device_in_db.id, session)
    session.commit()
