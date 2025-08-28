from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..routes.auth import get_current_user
from ..models.user import User
from ..models.driver import Driver
from ..schemas.driver import DriverCreate, DriverUpdate, Driver as DriverSchema

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverSchema)
def create_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar se CNH já existe
    db_driver = db.query(Driver).filter(Driver.cnh_number == driver.cnh_number).first()
    if db_driver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNH already registered"
        )
    
    db_driver = Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.get("/", response_model=List[DriverSchema])
def read_drivers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    drivers = db.query(Driver).offset(skip).limit(limit).all()
    return drivers


@router.get("/{driver_id}", response_model=DriverSchema)
def read_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.put("/{driver_id}", response_model=DriverSchema)
def update_driver(
    driver_id: int,
    driver: DriverUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    update_data = driver.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_driver, field, value)
    
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    db.delete(driver)
    db.commit()
    return {"message": "Driver deleted successfully"}