from datetime import datetime, timezone
from sqlmodel import select, Session
from db import get_session
from typing import List
from models.api_model import GPSData, Tour
from schemas.api_schema import DataRead


def get_data() -> List[GPSData]:
    with get_session() as session:
        stmt = select(GPSData).order_by(GPSData.timestamp.desc())
        return session.exec(stmt).all()


def check_tour(db: Session, tour_id: str) -> bool:
    stmt = select(Tour).where(Tour.tour_id == tour_id)
    tour = db.exec(stmt).first()
    if tour is None:
        return False 

    tour.last_seen_at = datetime.now(timezone.utc)
    return True


def save_points(db: Session, points: List[GPSData]) -> List[int]:
    db.add_all(points)
    db.flush()

    return [point.queue_id for point in points] 


def start_tour(created_tour: Tour) -> Tour:
    with get_session() as session:
        session.add(created_tour)
        session.commit()
        session.refresh(created_tour)
        return created_tour


def get_tours() -> List[Tour]:
    with get_session() as session:
        stmt = select(Tour).order_by(Tour.started_at.desc())
        return session.exec(stmt).all()
