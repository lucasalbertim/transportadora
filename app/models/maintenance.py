from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Float, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
from enum import Enum


class MaintenanceType(str, Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"


class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    maintenance_type = Column(String, nullable=False)  # MaintenanceType
    maintenance_date = Column(Date, nullable=False)
    cost = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    observations = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenances")