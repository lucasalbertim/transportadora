from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


class DriverBase(BaseModel):
    name: str
    cnh_number: str
    cnh_expiry: date
    phone: str
    email: Optional[EmailStr] = None
    address: str


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    cnh_number: Optional[str] = None
    cnh_expiry: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class Driver(DriverBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True