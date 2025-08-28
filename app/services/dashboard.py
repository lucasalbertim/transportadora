from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from models.trip import Trip, TripStatus
from models.client import Client
from models.driver import Driver
from models.vehicle import Vehicle
from models.route import Route
from models.maintenance import Maintenance, MaintenanceType
from schemas.dashboard import DashboardStats
from schemas.reports import (
    ClientRanking, 
    DriverRanking, 
    MaintenanceCosts, 
    ProfitabilityStats,
    DashboardV2
)


class DashboardService:
    @staticmethod
    def get_dashboard_stats(db: Session):
        # Contadores de viagens por status
        total_trips = db.query(Trip).count()
        planned_trips = db.query(Trip).filter(Trip.status == TripStatus.PLANNED).count()
        in_transit_trips = db.query(Trip).filter(Trip.status == TripStatus.IN_TRANSIT).count()
        completed_trips = db.query(Trip).filter(Trip.status == TripStatus.COMPLETED).count()
        cancelled_trips = db.query(Trip).filter(Trip.status == TripStatus.CANCELLED).count()
        
        # Contadores de cadastros
        total_clients = db.query(Client).count()
        total_drivers = db.query(Driver).count()
        total_vehicles = db.query(Vehicle).count()
        total_routes = db.query(Route).count()
        
        # Custos
        total_estimated_costs = db.query(
            func.sum(Trip.estimated_fuel_cost + Trip.estimated_toll_cost)
        ).scalar() or 0.0
        
        total_actual_costs = db.query(
            func.sum(func.coalesce(Trip.actual_fuel_cost, 0) + func.coalesce(Trip.actual_toll_cost, 0))
        ).scalar() or 0.0
        
        # Viagens recentes
        recent_trips = db.query(Trip).order_by(Trip.created_at.desc()).limit(10).all()
        recent_trips_data = []
        
        for trip in recent_trips:
            recent_trips_data.append({
                "id": trip.id,
                "client_name": trip.client.name,
                "driver_name": trip.driver.name,
                "vehicle_plate": trip.vehicle.plate,
                "status": trip.status.value,
                "departure_date": trip.departure_date.isoformat(),
                "estimated_arrival": trip.estimated_arrival.isoformat()
            })
        
        return DashboardStats(
            total_trips=total_trips,
            planned_trips=planned_trips,
            in_transit_trips=in_transit_trips,
            completed_trips=completed_trips,
            cancelled_trips=cancelled_trips,
            total_clients=total_clients,
            total_drivers=total_drivers,
            total_vehicles=total_vehicles,
            total_routes=total_routes,
            total_estimated_costs=total_estimated_costs,
            total_actual_costs=total_actual_costs,
            recent_trips=recent_trips_data
        )

    @staticmethod
    def get_dashboard_v2(db: Session) -> DashboardV2:
        """Dashboard avançado com métricas financeiras e rankings"""
        
        # Estatísticas básicas
        total_trips = db.query(Trip).count()
        trips_by_status = {
            "planned": db.query(Trip).filter(Trip.status == TripStatus.PLANNED).count(),
            "in_transit": db.query(Trip).filter(Trip.status == TripStatus.IN_TRANSIT).count(),
            "completed": db.query(Trip).filter(Trip.status == TripStatus.COMPLETED).count(),
            "cancelled": db.query(Trip).filter(Trip.status == TripStatus.CANCELLED).count()
        }
        
        # Métricas financeiras
        total_revenue = db.query(func.sum(func.coalesce(Trip.freight_revenue, 0))).scalar() or 0.0
        total_costs = db.query(
            func.sum(
                func.coalesce(Trip.actual_fuel_cost, 0) + 
                func.coalesce(Trip.actual_toll_cost, 0) + 
                func.coalesce(Trip.daily_allowance_cost, 0) + 
                func.coalesce(Trip.other_costs, 0)
            )
        ).scalar() or 0.0
        
        total_profit = total_revenue - total_costs
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Ranking de clientes
        client_ranking = db.query(
            Client.id,
            Client.name,
            func.count(Trip.id).label('total_trips'),
            func.sum(func.coalesce(Trip.freight_revenue, 0)).label('total_revenue'),
            func.sum(
                func.coalesce(Trip.freight_revenue, 0) - 
                func.coalesce(Trip.actual_fuel_cost, 0) - 
                func.coalesce(Trip.actual_toll_cost, 0) - 
                func.coalesce(Trip.daily_allowance_cost, 0) - 
                func.coalesce(Trip.other_costs, 0)
            ).label('total_profit')
        ).join(Trip).group_by(Client.id, Client.name).order_by(
            func.sum(
                func.coalesce(Trip.freight_revenue, 0) - 
                func.coalesce(Trip.actual_fuel_cost, 0) - 
                func.coalesce(Trip.actual_toll_cost, 0) - 
                func.coalesce(Trip.daily_allowance_cost, 0) - 
                func.coalesce(Trip.other_costs, 0)
            ).desc()
        ).limit(10).all()
        
        top_clients = [
            ClientRanking(
                client_id=row.id,
                client_name=row.name,
                total_trips=row.total_trips,
                total_revenue=float(row.total_revenue or 0),
                total_profit=float(row.total_profit or 0),
                average_profit_per_trip=float(row.total_profit or 0) / row.total_trips if row.total_trips > 0 else 0
            )
            for row in client_ranking
        ]
        
        # Ranking de motoristas
        driver_ranking = db.query(
            Driver.id,
            Driver.name,
            func.count(Trip.id).label('total_trips'),
            func.count(
                func.case((Trip.status == TripStatus.COMPLETED, 1))
            ).label('completed_trips'),
            func.sum(Route.estimated_distance).label('total_distance')
        ).join(Trip).join(Route).group_by(Driver.id, Driver.name).order_by(
            func.count(
                func.case((Trip.status == TripStatus.COMPLETED, 1))
            ).desc()
        ).limit(10).all()
        
        top_drivers = [
            DriverRanking(
                driver_id=row.id,
                driver_name=row.name,
                total_trips=row.total_trips,
                completed_trips=row.completed_trips,
                completion_rate=(row.completed_trips / row.total_trips * 100) if row.total_trips > 0 else 0,
                total_distance=float(row.total_distance or 0)
            )
            for row in driver_ranking
        ]
        
        # Custos de manutenção por veículo
        maintenance_costs = db.query(
            Maintenance.vehicle_id,
            Vehicle.plate,
            func.sum(Maintenance.cost).label('total_maintenance_cost'),
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
            ).label('corrective_cost'),
            func.count(Maintenance.id).label('maintenance_count')
        ).join(Vehicle).group_by(
            Maintenance.vehicle_id, 
            Vehicle.plate
        ).all()
        
        maintenance_costs_list = [
            MaintenanceCosts(
                vehicle_id=row.vehicle_id,
                vehicle_plate=row.plate,
                total_maintenance_cost=float(row.total_maintenance_cost or 0),
                preventive_cost=float(row.preventive_cost or 0),
                corrective_cost=float(row.corrective_cost or 0),
                maintenance_count=row.maintenance_count
            )
            for row in maintenance_costs
        ]
        
        # Tendência de lucratividade (últimos 6 meses)
        profitability_trend = []
        for i in range(6):
            # Simulação de dados mensais - em produção seria baseado em dados reais
            month_revenue = total_revenue / 6
            month_costs = total_costs / 6
            month_profit = month_revenue - month_costs
            month_margin = (month_profit / month_revenue * 100) if month_revenue > 0 else 0
            
            profitability_trend.append(
                ProfitabilityStats(
                    total_revenue=month_revenue,
                    total_costs=month_costs,
                    total_profit=month_profit,
                    profit_margin=month_margin,
                    period=f"Mês {i+1}"
                )
            )
        
        return DashboardV2(
            total_trips=total_trips,
            trips_by_status=trips_by_status,
            total_revenue=total_revenue,
            total_costs=total_costs,
            total_profit=total_profit,
            profit_margin=profit_margin,
            top_clients=top_clients,
            top_drivers=top_drivers,
            maintenance_costs=maintenance_costs_list,
            profitability_trend=profitability_trend
        )