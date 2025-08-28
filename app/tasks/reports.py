import os
import json
from datetime import datetime, date
from typing import Optional, Dict, Any
from celery import current_task
from core.celery_app import celery_app
from core.database import SessionLocal
from sqlalchemy.orm import Session
from models.trip import Trip, TripStatus
from models.maintenance import Maintenance, MaintenanceType
from models.client import Client
from models.driver import Driver
from models.vehicle import Vehicle
from models.route import Route
from core.config import settings


def get_db() -> Session:
    """Obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise


@celery_app.task(bind=True)
def generate_report_task(
    self,
    report_type: str,
    format: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    client_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    vehicle_id: Optional[int] = None
) -> Dict[str, Any]:
    """Tarefa para gerar relatórios em background"""
    
    try:
        # Atualizar progresso
        current_task.update_state(
            state='PROGRESS',
            meta={'progress': 10, 'message': 'Iniciando geração do relatório'}
        )
        
        db = get_db()
        
        # Converter datas
        start_dt = None
        end_dt = None
        if start_date:
            start_dt = datetime.fromisoformat(start_date).date()
        if end_date:
            end_dt = datetime.fromisoformat(end_date).date()
        
        # Atualizar progresso
        current_task.update_state(
            state='PROGRESS',
            meta={'progress': 30, 'message': 'Coletando dados'}
        )
        
        # Coletar dados baseado no tipo de relatório
        if report_type == "trips":
            data = generate_trips_report(db, start_dt, end_dt, client_id, driver_id, vehicle_id)
        elif report_type == "maintenance":
            data = generate_maintenance_report(db, start_dt, end_dt, vehicle_id)
        elif report_type == "financial":
            data = generate_financial_report(db, start_dt, end_dt, client_id)
        elif report_type == "profitability":
            data = generate_profitability_report(db, start_dt, end_dt)
        else:
            raise ValueError(f"Tipo de relatório não suportado: {report_type}")
        
        # Atualizar progresso
        current_task.update_state(
            state='PROGRESS',
            meta={'progress': 70, 'message': 'Gerando arquivo'}
        )
        
        # Gerar arquivo
        filename = generate_file(data, report_type, format)
        
        # Atualizar progresso
        current_task.update_state(
            state='PROGRESS',
            meta={'progress': 90, 'message': 'Finalizando'}
        )
        
        download_url = f"/reports/download/{filename}"
        
        return {
            "status": "success",
            "download_url": download_url,
            "filename": filename,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise
    finally:
        if 'db' in locals():
            db.close()


def generate_trips_report(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    client_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    vehicle_id: Optional[int] = None
) -> Dict[str, Any]:
    """Gerar relatório de viagens"""
    
    query = db.query(Trip).join(Client).join(Driver).join(Vehicle).join(Route)
    
    if start_date:
        query = query.filter(Trip.departure_date >= start_date)
    if end_date:
        query = query.filter(Trip.departure_date <= end_date)
    if client_id:
        query = query.filter(Trip.client_id == client_id)
    if driver_id:
        query = query.filter(Trip.driver_id == driver_id)
    if vehicle_id:
        query = query.filter(Trip.vehicle_id == vehicle_id)
    
    trips = query.all()
    
    return {
        "report_type": "trips",
        "filters": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "client_id": client_id,
            "driver_id": driver_id,
            "vehicle_id": vehicle_id
        },
        "total_trips": len(trips),
        "trips": [
            {
                "id": trip.id,
                "client_name": trip.client.name,
                "driver_name": trip.driver.name,
                "vehicle_plate": trip.vehicle.plate,
                "route_name": trip.route.name,
                "departure_date": trip.departure_date.isoformat(),
                "status": trip.status.value,
                "estimated_fuel_cost": trip.estimated_fuel_cost,
                "estimated_toll_cost": trip.estimated_toll_cost,
                "actual_fuel_cost": trip.actual_fuel_cost,
                "actual_toll_cost": trip.actual_toll_cost,
                "freight_revenue": trip.freight_revenue
            }
            for trip in trips
        ]
    }


def generate_maintenance_report(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    vehicle_id: Optional[int] = None
) -> Dict[str, Any]:
    """Gerar relatório de manutenções"""
    
    query = db.query(Maintenance).join(Vehicle)
    
    if start_date:
        query = query.filter(Maintenance.maintenance_date >= start_date)
    if end_date:
        query = query.filter(Maintenance.maintenance_date <= end_date)
    if vehicle_id:
        query = query.filter(Maintenance.vehicle_id == vehicle_id)
    
    maintenances = query.all()
    
    return {
        "report_type": "maintenance",
        "filters": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "vehicle_id": vehicle_id
        },
        "total_maintenances": len(maintenances),
        "maintenances": [
            {
                "id": maintenance.id,
                "vehicle_plate": maintenance.vehicle.plate,
                "vehicle_model": maintenance.vehicle.model,
                "maintenance_type": maintenance.maintenance_type,
                "maintenance_date": maintenance.maintenance_date.isoformat(),
                "cost": maintenance.cost,
                "description": maintenance.description,
                "is_completed": maintenance.is_completed
            }
            for maintenance in maintenances
        ]
    }


def generate_financial_report(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    client_id: Optional[int] = None
) -> Dict[str, Any]:
    """Gerar relatório financeiro"""
    
    query = db.query(Trip).join(Client)
    
    if start_date:
        query = query.filter(Trip.departure_date >= start_date)
    if end_date:
        query = query.filter(Trip.departure_date <= end_date)
    if client_id:
        query = query.filter(Trip.client_id == client_id)
    
    trips = query.all()
    
    total_revenue = sum(trip.freight_revenue or 0 for trip in trips)
    total_costs = sum(
        (trip.actual_fuel_cost or 0) + 
        (trip.actual_toll_cost or 0) + 
        (trip.daily_allowance_cost or 0) + 
        (trip.other_costs or 0)
        for trip in trips
    )
    total_profit = total_revenue - total_costs
    
    return {
        "report_type": "financial",
        "filters": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "client_id": client_id
        },
        "summary": {
            "total_revenue": total_revenue,
            "total_costs": total_costs,
            "total_profit": total_profit,
            "profit_margin": (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        },
        "trips": [
            {
                "id": trip.id,
                "client_name": trip.client.name,
                "freight_revenue": trip.freight_revenue or 0,
                "total_costs": (
                    (trip.actual_fuel_cost or 0) + 
                    (trip.actual_toll_cost or 0) + 
                    (trip.daily_allowance_cost or 0) + 
                    (trip.other_costs or 0)
                ),
                "profit": (trip.freight_revenue or 0) - (
                    (trip.actual_fuel_cost or 0) + 
                    (trip.actual_toll_cost or 0) + 
                    (trip.daily_allowance_cost or 0) + 
                    (trip.other_costs or 0)
                )
            }
            for trip in trips
        ]
    }


def generate_profitability_report(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Dict[str, Any]:
    """Gerar relatório de lucratividade"""
    
    # Implementação simplificada - em produção seria mais complexa
    return {
        "report_type": "profitability",
        "filters": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        },
        "message": "Relatório de lucratividade - implementação em desenvolvimento"
    }


def generate_file(data: Dict[str, Any], report_type: str, format: str) -> str:
    """Gerar arquivo do relatório"""
    
    # Criar diretório se não existir
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_type}_report_{timestamp}"
    
    if format == "json":
        filepath = os.path.join(settings.REPORTS_DIR, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"{filename}.json"
    
    elif format == "excel":
        # Implementação do Excel seria mais complexa
        filepath = os.path.join(settings.REPORTS_DIR, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"{filename}.json"
    
    elif format == "pdf":
        # Implementação do PDF seria mais complexa
        filepath = os.path.join(settings.REPORTS_DIR, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"{filename}.json"
    
    else:
        raise ValueError(f"Formato não suportado: {format}")