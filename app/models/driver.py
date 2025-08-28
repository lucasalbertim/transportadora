from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cnh_number = Column(String, unique=True, index=True, nullable=False)
    cnh_expiry = Column(Date, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    trips = relationship("Trip", back_populates="driver")