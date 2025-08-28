from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    plate = Column(String, index=True, nullable=False)  # Removido unique para multi-tenant
    model = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    capacity = Column(Float, nullable=False)  # Capacidade em toneladas
    fuel_type = Column(String, nullable=False)  # Diesel, Gasolina, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="vehicles")
    trips = relationship("Trip", back_populates="vehicle")
    maintenances = relationship("Maintenance", back_populates="vehicle")