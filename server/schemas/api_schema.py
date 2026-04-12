from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class UserResponse(BaseModel):
    username: str


class UserPost(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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
    tour_name: str
    device_id: str
    started_at: datetime
    last_seen_at: datetime


class TourUpdate(BaseModel):
    tour_name: str


class APIKeyData(BaseModel):
    device_id: int
    user_id: int

