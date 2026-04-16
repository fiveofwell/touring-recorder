from typing import List, Tuple
from sqlmodel import select, delete, Session
import sqlalchemy.dialects.sqlite as sqlite

from models.api_model import PointInDB, TourInDB, UserInDB, DeviceInDB, APIKeyInDB

def get_tour_by_client_tour_id(client_tour_id: str, session: Session) -> TourInDB | None:
    stmt = select(TourInDB).where(TourInDB.client_tour_id == client_tour_id)
    tour_in_db = session.exec(stmt).first()
    return tour_in_db


def get_points(tour_id: str, session: Session) -> List[PointInDB]:
    stmt = select(PointInDB).where(PointInDB.tour_id == tour_id).order_by(PointInDB.recorded_at.desc())
    return session.exec(stmt).all()


def add_tour(tour_in_db: TourInDB, session: Session) -> None:
    session.add(tour_in_db)


def upsert_points(points: List[PointInDB], session: Session) -> None:
    stmt = sqlite.insert(PointInDB).values([point.model_dump() for point in points]).on_conflict_do_nothing(
        index_elements=['tour_id', 'client_point_id']
    )
    session.exec(stmt)


def delete_tour(tour_id: int, session: Session) -> None:
    stmt = delete(TourInDB).where(TourInDB.id == tour_id)
    session.exec(stmt)


def delete_points(tour_id: int, session: Session) -> None:
    stmt = delete(PointInDB).where(PointInDB.tour_id == tour_id)
    session.exec(stmt)
    

def get_tours(user_id: int, session: Session) -> List[TourInDB]:
    stmt = select(TourInDB).where(TourInDB.user_id == user_id).order_by(TourInDB.created_at.desc())
    return session.exec(stmt).all()


def get_user(username: str, session: Session) -> UserInDB | None:
    stmt = select(UserInDB).where(UserInDB.username == username)
    return session.exec(stmt).first()


def add_user(user_in_db: UserInDB, session: Session) -> None:
    session.add(user_in_db)


def get_api_key(key_hash: str, session: Session) -> APIKeyInDB | None:
    stmt = select(APIKeyInDB).where(APIKeyInDB.key_hash == key_hash)
    return session.exec(stmt).first()


def get_device(device_id: str, session: Session) -> DeviceInDB | None:
    stmt = select(DeviceInDB).where(DeviceInDB.id == device_id)
    return session.exec(stmt).first()


def get_device_by_device_id(device_id: str, user_id: int, session: Session) -> DeviceInDB | None:
    stmt = select(DeviceInDB).where(DeviceInDB.device_id == device_id and DeviceInDB.user_id == user_id)
    return session.exec(stmt).first()


def get_device_by_device_name(device_name: str, user_id: int, session: Session) -> DeviceInDB | None:
    stmt = select(DeviceInDB).where(DeviceInDB.device_name == device_name and DeviceInDB.user_id == user_id)
    return session.exec(stmt).first()


def get_devices(user_id: int, session: Session) -> List[Tuple[DeviceInDB, APIKeyInDB]]:
    stmt = select(DeviceInDB, APIKeyInDB).join(APIKeyInDB, DeviceInDB.id == APIKeyInDB.device_id).where(DeviceInDB.user_id == user_id)
    return session.exec(stmt).all()


def add_device(device_in_db: DeviceInDB, session: Session) -> None:
    session.add(device_in_db)


def add_api_key(api_key_in_db: APIKeyInDB, session: Session) -> None:
    session.add(api_key_in_db)


def delete_device(device_id: int, session: Session) -> None:
    stmt = delete(DeviceInDB).where(DeviceInDB.id == device_id)
    session.exec(stmt)


def delete_api_key(device_id: int, session: Session) -> None:
    stmt = delete(APIKeyInDB).where(APIKeyInDB.device_id == device_id)
    session.exec(stmt)
