from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from models.maintenance import MaintenanceType


class MaintenanceBase(BaseModel):
    vehicle_id: int
    maintenance_type: MaintenanceType
    maintenance_date: date
    cost: float
    description: Optional[str] = None
    observations: Optional[str] = None
    is_completed: bool = False


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    maintenance_type: Optional[MaintenanceType] = None
    maintenance_date: Optional[date] = None
    cost: Optional[float] = None
    description: Optional[str] = None
    observations: Optional[str] = None
    is_completed: Optional[bool] = None


class Maintenance(MaintenanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaintenanceWithVehicle(Maintenance):
    vehicle_plate: str
    vehicle_model: str
    vehicle_brand: str