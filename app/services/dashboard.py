from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.trip import Trip, TripStatus
from ..models.client import Client
from ..models.driver import Driver
from ..models.vehicle import Vehicle
from ..models.route import Route
from ..schemas.dashboard import DashboardStats


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