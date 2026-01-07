import uuid
from typing import List
from datetime import datetime, timezone
from models.api_model import GPSData, Tour
from schemas.api_schema import Data, DataRead, TourRead, AcceptedData
from services.exceptions import UnauthorizedKey, TourNotFound
from repositories import api_repository
from db import get_session
import settings

API_KEY = settings.API_KEY

def get_data() -> List[DataRead]:
    return [DataRead.model_validate(e) for e in api_repository.get_data()]


def save_points(tour_id: str, points: List[Data], x_api_key: str) -> AcceptedData:
    if x_api_key != API_KEY:
        raise UnauthorizedKey()

    with get_session() as db:
        try:
            if not api_repository.check_tour(db, tour_id):
                raise TourNotFound()

            if not points:
                return AcceptedData(accepted_ids=[])
    
            points_in_db = [
                GPSData(
                    tour_id = tour_id,
                    device_id = point.device_id,
                    queue_id = point.queue_id,
                    latitude = point.latitude,
                    longitude = point.longitude,
                    timestamp = point.timestamp
                )
                for point in points
            ]
        
            accepted_ids = api_repository.save_points(db, points_in_db)
            db.commit()
            return AcceptedData(accepted_ids=accepted_ids)

        except Exception:
            db.rollback()
            raise 


def start_tour() -> TourRead:
    now_time = datetime.now(timezone.utc)
    tour = Tour(
        id = None,
        tour_id = str(uuid.uuid4()),
        started_at = now_time,
        last_seen_at = now_time
    )
    api_repository.start_tour(tour)
    return TourRead.model_validate(tour)


def get_tours() -> List[TourRead]:
    return [TourRead.model_validate(e) for e in api_repository.get_tours()]
