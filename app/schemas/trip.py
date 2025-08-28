from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.trip import TripStatus


class TripBase(BaseModel):
    client_id: int
    driver_id: int
    vehicle_id: int
    route_id: int
    departure_date: datetime
    estimated_arrival: datetime
    estimated_fuel_cost: float
    estimated_toll_cost: float
    actual_fuel_cost: Optional[float] = None
    actual_toll_cost: Optional[float] = None
    daily_allowance_cost: Optional[float] = None
    other_costs: Optional[float] = None
    freight_revenue: Optional[float] = None
    notes: Optional[str] = None


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    client_id: Optional[int] = None
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    route_id: Optional[int] = None
    departure_date: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: Optional[TripStatus] = None
    estimated_fuel_cost: Optional[float] = None
    estimated_toll_cost: Optional[float] = None
    actual_fuel_cost: Optional[float] = None
    actual_toll_cost: Optional[float] = None
    daily_allowance_cost: Optional[float] = None
    other_costs: Optional[float] = None
    freight_revenue: Optional[float] = None
    notes: Optional[str] = None


class Trip(TripBase):
    id: int
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: TripStatus
    actual_fuel_cost: Optional[float] = None
    actual_toll_cost: Optional[float] = None
    daily_allowance_cost: Optional[float] = None
    other_costs: Optional[float] = None
    freight_revenue: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TripWithRelations(Trip):
    client_name: str
    driver_name: str
    vehicle_plate: str
    route_name: str

    class Config:
        from_attributes = True