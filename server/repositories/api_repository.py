from typing import List
from sqlmodel import select, delete, Session
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


def upsert_points(points: List[PointInDB], session: Session) -> None:
    stmt = sqlite.insert(PointInDB).values([point.model_dump() for point in points]).on_conflict_do_nothing(
        index_elements=['tour_id', 'client_point_id']
    )
    session.exec(stmt)
    return None


def delete_tour(tour_id: str, session: Session) -> None:
    stmt = delete(TourInDB).where(TourInDB.tour_id == tour_id)
    session.exec(stmt)
    return None


def delete_points(tour_id: str, session: Session) -> None:
    stmt = delete(PointInDB).where(PointInDB.tour_id == tour_id)
    session.exec(stmt)
    return None
    

def get_tours(session: Session) -> List[TourInDB]:
    stmt = select(TourInDB).order_by(TourInDB.started_at.desc())
    return session.exec(stmt).all()
