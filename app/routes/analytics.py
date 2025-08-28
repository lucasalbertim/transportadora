from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from routes.auth import get_current_user
from models.user import User
from models.tenant import Tenant
from core.tenant import get_current_tenant
from services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/customer-retention")
def get_customer_retention(
    period_days: int = Query(90, ge=30, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter taxa de retenção de clientes"""
    analytics = AnalyticsService(db)
    return analytics.get_customer_retention_rate(current_tenant.id, period_days)


@router.get("/fleet-occupation")
def get_fleet_occupation(
    period_days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter taxa de ocupação da frota"""
    analytics = AnalyticsService(db)
    return analytics.get_fleet_occupation_rate(current_tenant.id, period_days)


@router.get("/cost-per-km")
def get_cost_per_km(
    period_days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter custo médio por km rodado"""
    analytics = AnalyticsService(db)
    return analytics.get_average_cost_per_km(current_tenant.id, period_days)


@router.get("/future-earnings")
def get_future_earnings(
    months: int = Query(6, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter projeção de ganhos futuros"""
    analytics = AnalyticsService(db)
    return analytics.get_future_earnings_projection(current_tenant.id, months)


@router.get("/on-time-delivery")
def get_on_time_delivery(
    period_days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter análise de viagens no prazo vs atrasadas"""
    analytics = AnalyticsService(db)
    return analytics.get_on_time_delivery_analysis(current_tenant.id, period_days)


@router.get("/maintenance-costs")
def get_maintenance_costs(
    period_days: int = Query(90, ge=30, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter análise de custos de manutenção"""
    analytics = AnalyticsService(db)
    return analytics.get_maintenance_cost_analysis(current_tenant.id, period_days)


@router.get("/driver-performance")
def get_driver_performance(
    period_days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter métricas de performance dos motoristas"""
    analytics = AnalyticsService(db)
    return analytics.get_driver_performance_metrics(current_tenant.id, period_days)


@router.get("/comprehensive")
def get_comprehensive_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Obter analytics completo com todos os KPIs"""
    analytics = AnalyticsService(db)
    return analytics.get_comprehensive_analytics(current_tenant.id)