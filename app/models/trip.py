from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
import enum


class TripStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    
    departure_date = Column(DateTime, nullable=False)
    estimated_arrival = Column(DateTime, nullable=False)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)
    
    status = Column(Enum(TripStatus), default=TripStatus.PLANNED)
    
    # Custos
    estimated_fuel_cost = Column(Float, nullable=False)
    estimated_toll_cost = Column(Float, nullable=False)
    actual_fuel_cost = Column(Float, nullable=True)
    actual_toll_cost = Column(Float, nullable=True)
    daily_allowance_cost = Column(Float, nullable=True)
    other_costs = Column(Float, nullable=True)
    freight_revenue = Column(Float, nullable=True)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")
    vehicle = relationship("Vehicle", back_populates="trips")
    route = relationship("Route", back_populates="trips")