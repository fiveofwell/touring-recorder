from datetime import datetime
from sqlmodel import SQLModel, Field, UniqueConstraint, Index

class PointInDB(SQLModel, table=True):
    __table_args__=(
        UniqueConstraint("tour_id", "client_point_id", name="unique_tour_client_point"),
        Index("idx_tour_recorded_at", "tour_id", "recorded_at"),
    )

    id: int | None = Field(default=None, primary_key=True)
    tour_id: int = Field(foreign_key="tourindb.id")
    client_point_id: int
    latitude: float
    longitude: float
    recorded_at: datetime


class TourInDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    client_tour_id: str = Field(unique=True)
    tour_name: str
    # ブラウザからのダミー登録の場合はNULL
    device_id: int | None = Field(default=None, foreign_key="deviceindb.id")
    # device_idがNULLのダミーデータでもuser_idを辿れるよう非正規化
    user_id: int = Field(foreign_key="userindb.id")
    created_at: datetime = Field(index=True)
    updated_at: datetime


class UserInDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    disabled: bool = Field(default=False)


class DeviceInDB(SQLModel, table=True):
    __table_args__=(
        UniqueConstraint("user_id", "device_name", name="unique_user_id_device_name"),
    )

    id: int | None = Field(default=None, primary_key=True)
    device_id: str = Field(index=True)
    user_id: int = Field(foreign_key="userindb.id")
    device_name: str


class APIKeyInDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    device_id: int = Field(foreign_key="deviceindb.id")
    key_hash: str = Field(unique=True, index=True)
    key_prefix: str
    created_at: datetime
    last_used_at: datetime | None = Field(default=None)
    disabled: bool = Field(default=False)
