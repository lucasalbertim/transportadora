from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..routes.auth import get_current_user
from ..models.user import User
from ..models.trip import Trip, TripStatus
from ..models.client import Client
from ..models.driver import Driver
from ..models.vehicle import Vehicle
from ..models.route import Route
from ..schemas.trip import TripCreate, TripUpdate, Trip as TripSchema, TripWithRelations

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/", response_model=TripSchema)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar se as entidades relacionadas existem
    client = db.query(Client).filter(Client.id == trip.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    route = db.query(Route).filter(Route.id == trip.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db_trip = Trip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.get("/", response_model=List[TripWithRelations])
def read_trips(
    skip: int = 0,
    limit: int = 100,
    status: TripStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Trip)
    if status:
        query = query.filter(Trip.status == status)
    
    trips = query.offset(skip).limit(limit).all()
    
    # Adicionar informações das relações
    result = []
    for trip in trips:
        trip_data = TripWithRelations(
            **trip.__dict__,
            client_name=trip.client.name,
            driver_name=trip.driver.name,
            vehicle_plate=trip.vehicle.plate,
            route_name=trip.route.name
        )
        result.append(trip_data)
    
    return result


@router.get("/{trip_id}", response_model=TripWithRelations)
def read_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return TripWithRelations(
        **trip.__dict__,
        client_name=trip.client.name,
        driver_name=trip.driver.name,
        vehicle_plate=trip.vehicle.plate,
        route_name=trip.route.name
    )


@router.put("/{trip_id}", response_model=TripSchema)
def update_trip(
    trip_id: int,
    trip: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    update_data = trip.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_trip, field, value)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.patch("/{trip_id}/status")
def update_trip_status(
    trip_id: int,
    status: TripStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db_trip.status = status
    
    # Atualizar timestamps baseado no status
    if status == TripStatus.IN_TRANSIT and not db_trip.actual_departure:
        from datetime import datetime
        db_trip.actual_departure = datetime.utcnow()
    elif status == TripStatus.COMPLETED and not db_trip.actual_arrival:
        from datetime import datetime
        db_trip.actual_arrival = datetime.utcnow()
    
    db.commit()
    db.refresh(db_trip)
    return {"message": f"Trip status updated to {status.value}"}


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}