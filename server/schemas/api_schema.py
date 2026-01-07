from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class DataRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    device_id: str
    tour_id: str
    latitude: float
    longitude: float
    timestamp: datetime


class AcceptedData(BaseModel):
    accepted_ids: List[int]


class Data(BaseModel):
    queue_id: int
    device_id: str
    latitude: float
    longitude: float
    timestamp: datetime


class DataPost(BaseModel):
    tour_id: str
    points: List[Data]


class TourRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tour_id: str
    started_at: datetime
    last_seen_at: datetime

