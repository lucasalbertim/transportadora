from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class ReportType(str, Enum):
    TRIPS = "trips"
    MAINTENANCE = "maintenance"
    FINANCIAL = "financial"
    PROFITABILITY = "profitability"


class ReportFormat(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"


class ReportRequest(BaseModel):
    report_type: ReportType
    format: ReportFormat
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    client_id: Optional[int] = None
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None


class ReportStatus(BaseModel):
    task_id: str
    status: str
    progress: Optional[int] = None
    download_url: Optional[str] = None


class ProfitabilityStats(BaseModel):
    total_revenue: float
    total_costs: float
    total_profit: float
    profit_margin: float
    period: str


class ClientRanking(BaseModel):
    client_id: int
    client_name: str
    total_trips: int
    total_revenue: float
    total_profit: float
    average_profit_per_trip: float


class DriverRanking(BaseModel):
    driver_id: int
    driver_name: str
    total_trips: int
    completed_trips: int
    completion_rate: float
    total_distance: float


class MaintenanceCosts(BaseModel):
    vehicle_id: int
    vehicle_plate: str
    total_maintenance_cost: float
    preventive_cost: float
    corrective_cost: float
    maintenance_count: int


class DashboardV2(BaseModel):
    total_trips: int
    trips_by_status: dict
    total_revenue: float
    total_costs: float
    total_profit: float
    profit_margin: float
    top_clients: List[ClientRanking]
    top_drivers: List[DriverRanking]
    maintenance_costs: List[MaintenanceCosts]
    profitability_trend: List[ProfitabilityStats]