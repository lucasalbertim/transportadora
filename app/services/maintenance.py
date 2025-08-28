from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from models.maintenance import Maintenance, MaintenanceType
from models.vehicle import Vehicle
from schemas.maintenance import MaintenanceCreate, MaintenanceUpdate, MaintenanceWithVehicle


class MaintenanceService:
    @staticmethod
    def create_maintenance(db: Session, maintenance: MaintenanceCreate) -> Maintenance:
        db_maintenance = Maintenance(**maintenance.dict())
        db.add(db_maintenance)
        db.commit()
        db.refresh(db_maintenance)
        return db_maintenance

    @staticmethod
    def get_maintenance(db: Session, maintenance_id: int) -> Optional[Maintenance]:
        return db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    @staticmethod
    def get_maintenances(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        vehicle_id: Optional[int] = None,
        maintenance_type: Optional[MaintenanceType] = None
    ) -> List[Maintenance]:
        query = db.query(Maintenance)
        
        if vehicle_id:
            query = query.filter(Maintenance.vehicle_id == vehicle_id)
        
        if maintenance_type:
            query = query.filter(Maintenance.maintenance_type == maintenance_type)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_maintenance(
        db: Session, 
        maintenance_id: int, 
        maintenance: MaintenanceUpdate
    ) -> Optional[Maintenance]:
        db_maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not db_maintenance:
            return None
        
        update_data = maintenance.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_maintenance, field, value)
        
        db.commit()
        db.refresh(db_maintenance)
        return db_maintenance

    @staticmethod
    def delete_maintenance(db: Session, maintenance_id: int) -> bool:
        db_maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not db_maintenance:
            return False
        
        db.delete(db_maintenance)
        db.commit()
        return True

    @staticmethod
    def get_maintenance_costs_by_vehicle(db: Session) -> List[dict]:
        """Retorna custos de manutenção por veículo"""
        result = db.query(
            Maintenance.vehicle_id,
            Vehicle.plate,
            Vehicle.model,
            Vehicle.brand,
            func.sum(Maintenance.cost).label('total_cost'),
            func.count(Maintenance.id).label('maintenance_count'),
            func.sum(
                func.case(
                    (Maintenance.maintenance_type == MaintenanceType.PREVENTIVE, Maintenance.cost),
                    else_=0
                )
            ).label('preventive_cost'),
            func.sum(
                func.case(
                    (Maintenance.maintenance_type == MaintenanceType.CORRECTIVE, Maintenance.cost),
                    else_=0
                )
            ).label('corrective_cost')
        ).join(Vehicle).group_by(
            Maintenance.vehicle_id, 
            Vehicle.plate, 
            Vehicle.model, 
            Vehicle.brand
        ).all()
        
        return [
            {
                "vehicle_id": row.vehicle_id,
                "vehicle_plate": row.plate,
                "vehicle_model": row.model,
                "vehicle_brand": row.brand,
                "total_maintenance_cost": float(row.total_cost or 0),
                "preventive_cost": float(row.preventive_cost or 0),
                "corrective_cost": float(row.corrective_cost or 0),
                "maintenance_count": row.maintenance_count
            }
            for row in result
        ]

    @staticmethod
    def get_maintenance_with_vehicle_info(
        db: Session, 
        maintenance_id: int
    ) -> Optional[MaintenanceWithVehicle]:
        result = db.query(
            Maintenance, 
            Vehicle.plate, 
            Vehicle.model, 
            Vehicle.brand
        ).join(Vehicle).filter(Maintenance.id == maintenance_id).first()
        
        if not result:
            return None
        
        maintenance, plate, model, brand = result
        return MaintenanceWithVehicle(
            **maintenance.__dict__,
            vehicle_plate=plate,
            vehicle_model=model,
            vehicle_brand=brand
        )