from typing import List
from datetime import datetime, timezone
from sqlmodel import select, Session
import sqlalchemy.dialects.sqlite as sqlite

from models.api_model import PointInDB, TourInDB

def get_tour(tour_id: str, session: Session) -> TourInDB | None:
    stmt = select(TourInDB).where(TourInDB.tour_id == tour_id)
    tour_in_db = session.exec(stmt).first()
    return tour_in_db


def get_points(tour_id: str, session: Session) -> List[PointInDB]:
    stmt = select(PointInDB).where(PointInDB.tour_id == tour_id).order_by(PointInDB.timestamp.desc())
    return session.exec(stmt).all()


def add_tour(tour_in_db: TourInDB, session: Session) -> None:
    session.add(tour_in_db)
    return None

def touch_tour(tour_id: str, session: Session) -> None:
    tour_in_db = get_tour(tour_id, session)
    if tour_in_db is not None:
        tour_in_db.last_seen_at = datetime.now(timezone.utc)
    return None


def upsert_points(points: List[PointInDB], session: Session) -> None:
    values = [
        {
            "device_id": point.device_id,
            "tour_id": point.tour_id,
            "client_point_id": point.client_point_id,
            "latitude": point.latitude,
            "longitude": point.longitude,
            "timestamp": point.timestamp,
        }
        for point in points
    ]

    stmt = sqlite.insert(PointInDB).values(values).on_conflict_do_nothing(
        index_elements=['tour_id', 'client_point_id']
    )
    session.exec(stmt)
    return None


def get_tours(session: Session) -> List[TourInDB]:
    stmt = select(TourInDB).order_by(TourInDB.started_at.desc())
    return session.exec(stmt).all()
