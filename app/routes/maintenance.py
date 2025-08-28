from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.maintenance import (
    Maintenance, 
    MaintenanceCreate, 
    MaintenanceUpdate, 
    MaintenanceWithVehicle
)
from services.maintenance import MaintenanceService

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post("/", response_model=Maintenance)
def create_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar nova manutenção"""
    return MaintenanceService.create_maintenance(db, maintenance)


@router.get("/", response_model=List[Maintenance])
def get_maintenances(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vehicle_id: Optional[int] = Query(None),
    maintenance_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar manutenções com filtros opcionais"""
    return MaintenanceService.get_maintenances(
        db, skip=skip, limit=limit, 
        vehicle_id=vehicle_id, 
        maintenance_type=maintenance_type
    )


@router.get("/{maintenance_id}", response_model=MaintenanceWithVehicle)
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter manutenção específica com informações do veículo"""
    maintenance = MaintenanceService.get_maintenance_with_vehicle_info(db, maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return maintenance


@router.put("/{maintenance_id}", response_model=Maintenance)
def update_maintenance(
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar manutenção"""
    updated_maintenance = MaintenanceService.update_maintenance(db, maintenance_id, maintenance)
    if not updated_maintenance:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return updated_maintenance


@router.delete("/{maintenance_id}")
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar manutenção"""
    success = MaintenanceService.delete_maintenance(db, maintenance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return {"message": "Manutenção deletada com sucesso"}


@router.get("/reports/costs-by-vehicle")
def get_maintenance_costs_by_vehicle(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Relatório de custos de manutenção por veículo"""
    return MaintenanceService.get_maintenance_costs_by_vehicle(db)