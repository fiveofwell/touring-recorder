from datetime import datetime
from sqlmodel import SQLModel, Field

class GPSData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tour_id: str = Field(foreign_key="tour.tour_id", index=True)
    device_id: str
    queue_id: int
    latitude: float
    longitude: float
    timestamp: datetime


class Tour(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tour_id: str = Field(unique=True, index=True)
    started_at: datetime = Field(index=True)
    last_seen_at: datetime
