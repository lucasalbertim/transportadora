from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VehicleBase(BaseModel):
    plate: str
    model: str
    brand: str
    year: int
    capacity: float
    fuel_type: str


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    plate: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    year: Optional[int] = None
    capacity: Optional[float] = None
    fuel_type: Optional[str] = None
    is_active: Optional[bool] = None


class Vehicle(VehicleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True