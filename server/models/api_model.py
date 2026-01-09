from datetime import datetime
from sqlmodel import SQLModel, Field, UniqueConstraint 

class PointInDB(SQLModel, table=True):
    __table_args__=(
        UniqueConstraint("tour_id", "client_point_id", name="unique_tour_client_point"),
    )

    id: int | None = Field(default=None, primary_key=True)
    device_id: str
    tour_id: str = Field(foreign_key="tourindb.tour_id", index=True)
    client_point_id: str 
    latitude: float
    longitude: float
    timestamp: datetime


class TourInDB(SQLModel, table=True):
    tour_id: str = Field(primary_key=True, index=True)
    device_id: str
    started_at: datetime = Field(index=True)
    last_seen_at: datetime
