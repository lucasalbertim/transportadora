from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RouteBase(BaseModel):
    name: str
    origin: str
    destination: str
    estimated_distance: float
    estimated_time: float
    description: Optional[str] = None


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    name: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    estimated_distance: Optional[float] = None
    estimated_time: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class Route(RouteBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True