from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    domain = Column(String, unique=True, nullable=True)
    
    # Configurações da empresa
    company_name = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Configurações do sistema
    max_users = Column(Integer, default=10)
    max_vehicles = Column(Integer, default=50)
    features_enabled = Column(Text, nullable=True)  # JSON string
    
    # Status
    is_active = Column(Boolean, default=True)
    is_trial = Column(Boolean, default=True)
    trial_ends_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="tenant")
    clients = relationship("Client", back_populates="tenant")
    drivers = relationship("Driver", back_populates="tenant")
    vehicles = relationship("Vehicle", back_populates="tenant")
    routes = relationship("Route", back_populates="tenant")
    trips = relationship("Trip", back_populates="tenant")
    maintenances = relationship("Maintenance", back_populates="tenant")