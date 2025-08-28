from pydantic import BaseModel
from typing import Dict, Any


class DashboardStats(BaseModel):
    total_trips: int
    planned_trips: int
    in_transit_trips: int
    completed_trips: int
    cancelled_trips: int
    total_clients: int
    total_drivers: int
    total_vehicles: int
    total_routes: int
    total_estimated_costs: float
    total_actual_costs: float
    recent_trips: list[Dict[str, Any]]