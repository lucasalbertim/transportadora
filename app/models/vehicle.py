from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from ..core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True, index=True, nullable=False)
    model = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    capacity = Column(Float, nullable=False)  # Capacidade em toneladas
    fuel_type = Column(String, nullable=False)  # Diesel, Gasolina, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())