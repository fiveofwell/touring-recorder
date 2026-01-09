from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Point(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    client_point_id: int
    latitude: float
    longitude: float
    timestamp: datetime


class PointsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    device_id: str
    points: List[Point]


class PointsPost(BaseModel):
    device_id: str
    points: List[Point]


class SavePointsResult(BaseModel):
    ok: bool


class TourResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tour_id: str
    device_id: str
    started_at: datetime
    last_seen_at: datetime

