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
    recorded_at: datetime


class PointsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    points: List[Point]


class PointsPost(BaseModel):
    points: List[Point]


class SavePointsResult(BaseModel):
    ok: bool


class TourResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    client_tour_id: str
    tour_name: str
    device_name: str | None = None
    created_at: datetime
    updated_at: datetime


class TourUpdate(BaseModel):
    tour_name: str


class APIKeyData(BaseModel):
    device_id: int
    user_id: int


class APIKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key_prefix: str
    created_at: datetime
    last_used_at: datetime | None = None


class DeviceFirstResponse(BaseModel):
    device_id: str
    device_name: str
    api_key: str
    

class DeviceResponse(BaseModel):
    device_id: str
    device_name: str
    api_key: APIKeyResponse


class DevicePost(BaseModel):
    device_name: str



