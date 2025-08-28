from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.reports import ReportRequest, ReportStatus, DashboardV2
from services.dashboard import DashboardService
from tasks.reports import generate_report_task

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate", response_model=ReportStatus)
def generate_report(
    report_request: ReportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Solicitar geração de relatório em background"""
    task = generate_report_task.delay(
        report_type=report_request.report_type.value,
        format=report_request.format.value,
        start_date=report_request.start_date.isoformat() if report_request.start_date else None,
        end_date=report_request.end_date.isoformat() if report_request.end_date else None,
        client_id=report_request.client_id,
        driver_id=report_request.driver_id,
        vehicle_id=report_request.vehicle_id
    )
    
    return ReportStatus(
        task_id=task.id,
        status="PENDING",
        progress=0
    )


@router.get("/status/{task_id}", response_model=ReportStatus)
def get_report_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Verificar status de um relatório"""
    from core.celery_app import celery_app
    
    task_result = celery_app.AsyncResult(task_id)
    
    if task_result.ready():
        if task_result.successful():
            return ReportStatus(
                task_id=task_id,
                status="COMPLETED",
                progress=100,
                download_url=task_result.result.get("download_url")
            )
        else:
            return ReportStatus(
                task_id=task_id,
                status="FAILED",
                progress=0
            )
    else:
        return ReportStatus(
            task_id=task_id,
            status="PENDING",
            progress=task_result.info.get("progress", 0) if task_result.info else 0
        )


@router.get("/dashboard/v2", response_model=DashboardV2)
def get_dashboard_v2(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dashboard avançado com métricas financeiras e rankings"""
    return DashboardService.get_dashboard_v2(db)