from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, date
from models.trip import Trip, TripStatus
from models.client import Client
from models.driver import Driver
from models.vehicle import Vehicle
from models.maintenance import Maintenance, MaintenanceType
from core.logging import get_logger

logger = get_logger("analytics")


class AnalyticsService:
    """Serviço de analytics e KPIs avançados"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_customer_retention_rate(self, tenant_id: int, period_days: int = 90) -> Dict[str, Any]:
        """Calcular taxa de retenção de clientes"""
        
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Clientes ativos no período
        active_clients = self.db.query(Client).filter(
            and_(
                Client.tenant_id == tenant_id,
                Client.created_at <= start_date
            )
        ).subquery()
        
        # Clientes que fizeram viagens no período
        retained_clients = self.db.query(Trip.client_id).filter(
            and_(
                Trip.tenant_id == tenant_id,
                Trip.created_at >= start_date
            )
        ).distinct().subquery()
        
        # Calcular retenção
        total_old_clients = self.db.query(active_clients).count()
        retained_count = self.db.query(retained_clients).count()
        
        retention_rate = (retained_count / total_old_clients * 100) if total_old_clients > 0 else 0
        
        return {
            "retention_rate": round(retention_rate, 2),
            "total_old_clients": total_old_clients,
            "retained_clients": retained_count,
            "period_days": period_days
        }
    
    def get_fleet_occupation_rate(self, tenant_id: int, period_days: int = 30) -> Dict[str, Any]:
        """Calcular taxa de ocupação da frota"""
        
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Total de veículos
        total_vehicles = self.db.query(Vehicle).filter(
            Vehicle.tenant_id == tenant_id
        ).count()
        
        # Veículos que fizeram viagens no período
        active_vehicles = self.db.query(Trip.vehicle_id).filter(
            and_(
                Trip.tenant_id == tenant_id,
                Trip.created_at >= start_date
            )
        ).distinct().count()
        
        occupation_rate = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
        
        return {
            "occupation_rate": round(occupation_rate, 2),
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "period_days": period_days
        }
    
    def get_average_cost_per_km(self, tenant_id: int, period_days: int = 30) -> Dict[str, Any]:
        """Calcular custo médio por km rodado"""
        
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Viagens completadas no período
        completed_trips = self.db.query(Trip).filter(
            and_(
                Trip.tenant_id == tenant_id,
                Trip.status == TripStatus.COMPLETED,
                Trip.created_at >= start_date
            )
        ).all()
        
        total_cost = 0
        total_distance = 0
        
        for trip in completed_trips:
            # Calcular custo total da viagem
            trip_cost = (
                (trip.actual_fuel_cost or 0) +
                (trip.actual_toll_cost or 0) +
                (trip.daily_allowance_cost or 0) +
                (trip.other_costs or 0)
            )
            
            # Obter distância da rota
            route_distance = trip.route.estimated_distance if trip.route else 0
            
            total_cost += trip_cost
            total_distance += route_distance
        
        avg_cost_per_km = (total_cost / total_distance) if total_distance > 0 else 0
        
        return {
            "average_cost_per_km": round(avg_cost_per_km, 2),
            "total_cost": round(total_cost, 2),
            "total_distance": round(total_distance, 2),
            "completed_trips": len(completed_trips),
            "period_days": period_days
        }
    
    def get_future_earnings_projection(self, tenant_id: int, months: int = 6) -> Dict[str, Any]:
        """Projeção de ganhos futuros"""
        
        # Calcular média de receita mensal dos últimos 3 meses
        three_months_ago = datetime.now() - timedelta(days=90)
        
        monthly_revenues = []
        for i in range(3):
            month_start = three_months_ago + timedelta(days=i*30)
            month_end = month_start + timedelta(days=30)
            
            month_revenue = self.db.query(func.sum(Trip.freight_revenue)).filter(
                and_(
                    Trip.tenant_id == tenant_id,
                    Trip.created_at >= month_start,
                    Trip.created_at < month_end
                )
            ).scalar() or 0
            
            monthly_revenues.append(month_revenue)
        
        avg_monthly_revenue = sum(monthly_revenues) / len(monthly_revenues) if monthly_revenues else 0
        
        # Projeção para os próximos meses
        projections = []
        for i in range(months):
            month_date = datetime.now() + timedelta(days=i*30)
            projected_revenue = avg_monthly_revenue * (1 + (i * 0.05))  # 5% de crescimento mensal
            
            projections.append({
                "month": month_date.strftime("%Y-%m"),
                "projected_revenue": round(projected_revenue, 2),
                "growth_rate": round(5 * (i + 1), 2)
            })
        
        return {
            "average_monthly_revenue": round(avg_monthly_revenue, 2),
            "projections": projections,
            "total_projected_revenue": round(sum(p["projected_revenue"] for p in projections), 2)
        }
    
    def get_on_time_delivery_analysis(self, tenant_id: int, period_days: int = 30) -> Dict[str, Any]:
        """Análise de viagens no prazo vs atrasadas"""
        
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Viagens completadas no período
        completed_trips = self.db.query(Trip).filter(
            and_(
                Trip.tenant_id == tenant_id,
                Trip.status == TripStatus.COMPLETED,
                Trip.created_at >= start_date
            )
        ).all()
        
        on_time_count = 0
        delayed_count = 0
        
        for trip in completed_trips:
            if trip.actual_arrival and trip.estimated_arrival:
                if trip.actual_arrival <= trip.estimated_arrival:
                    on_time_count += 1
                else:
                    delayed_count += 1
        
        total_trips = on_time_count + delayed_count
        on_time_rate = (on_time_count / total_trips * 100) if total_trips > 0 else 0
        
        return {
            "on_time_rate": round(on_time_rate, 2),
            "on_time_trips": on_time_count,
            "delayed_trips": delayed_count,
            "total_trips": total_trips,
            "period_days": period_days
        }
    
    def get_maintenance_cost_analysis(self, tenant_id: int, period_days: int = 90) -> Dict[str, Any]:
        """Análise de custos de manutenção"""
        
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Manutenções no período
        maintenances = self.db.query(Maintenance).join(Vehicle).filter(
            and_(
                Vehicle.tenant_id == tenant_id,
                Maintenance.maintenance_date >= start_date
            )
        ).all()
        
        preventive_cost = 0
        corrective_cost = 0
        
        for maintenance in maintenances:
            if maintenance.maintenance_type == MaintenanceType.PREVENTIVE:
                preventive_cost += maintenance.cost
            else:
                corrective_cost += maintenance.cost
        
        total_cost = preventive_cost + corrective_cost
        
        return {
            "total_maintenance_cost": round(total_cost, 2),
            "preventive_cost": round(preventive_cost, 2),
            "corrective_cost": round(corrective_cost, 2),
            "preventive_percentage": round((preventive_cost / total_cost * 100) if total_cost > 0 else 0, 2),
            "corrective_percentage": round((corrective_cost / total_cost * 100) if total_cost > 0 else 0, 2),
            "total_maintenances": len(maintenances),
            "period_days": period_days
        }
    
    def get_driver_performance_metrics(self, tenant_id: int, period_days: int = 30) -> List[Dict[str, Any]]:
        """Métricas de performance dos motoristas"""
        
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Estatísticas por motorista
        driver_stats = self.db.query(
            Driver.id,
            Driver.name,
            func.count(Trip.id).label('total_trips'),
            func.count(
                func.case((Trip.status == TripStatus.COMPLETED, 1))
            ).label('completed_trips'),
            func.sum(func.coalesce(Trip.freight_revenue, 0)).label('total_revenue'),
            func.avg(func.coalesce(Trip.actual_fuel_cost, 0)).label('avg_fuel_cost')
        ).join(Trip).filter(
            and_(
                Driver.tenant_id == tenant_id,
                Trip.created_at >= start_date
            )
        ).group_by(Driver.id, Driver.name).all()
        
        results = []
        for stat in driver_stats:
            completion_rate = (stat.completed_trips / stat.total_trips * 100) if stat.total_trips > 0 else 0
            
            results.append({
                "driver_id": stat.id,
                "driver_name": stat.name,
                "total_trips": stat.total_trips,
                "completed_trips": stat.completed_trips,
                "completion_rate": round(completion_rate, 2),
                "total_revenue": round(float(stat.total_revenue or 0), 2),
                "average_fuel_cost": round(float(stat.avg_fuel_cost or 0), 2)
            })
        
        return results
    
    def get_comprehensive_analytics(self, tenant_id: int) -> Dict[str, Any]:
        """Analytics completo com todos os KPIs"""
        
        return {
            "customer_retention": self.get_customer_retention_rate(tenant_id),
            "fleet_occupation": self.get_fleet_occupation_rate(tenant_id),
            "cost_per_km": self.get_average_cost_per_km(tenant_id),
            "future_earnings": self.get_future_earnings_projection(tenant_id),
            "on_time_delivery": self.get_on_time_delivery_analysis(tenant_id),
            "maintenance_costs": self.get_maintenance_cost_analysis(tenant_id),
            "driver_performance": self.get_driver_performance_metrics(tenant_id)
        }