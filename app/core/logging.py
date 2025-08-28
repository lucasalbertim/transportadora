import structlog
import logging
import sys
from typing import Any, Dict
from core.config import settings


def setup_logging():
    """Configurar logging estruturado"""
    
    # Configurar structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configurar logging padrão
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper())
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Obter logger estruturado"""
    return structlog.get_logger(name)


class RequestLogger:
    """Logger para requisições HTTP"""
    
    def __init__(self, logger: structlog.BoundLogger = None):
        self.logger = logger or get_logger("http")
    
    def log_request(self, request, tenant_id: str = None, user_id: str = None):
        """Log de requisição recebida"""
        self.logger.info(
            "request_received",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            tenant_id=tenant_id,
            user_id=user_id
        )
    
    def log_response(self, request, response, tenant_id: str = None, user_id: str = None):
        """Log de resposta enviada"""
        self.logger.info(
            "response_sent",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            tenant_id=tenant_id,
            user_id=user_id
        )
    
    def log_error(self, request, error, tenant_id: str = None, user_id: str = None):
        """Log de erro"""
        self.logger.error(
            "request_error",
            method=request.method,
            url=str(request.url),
            error_type=type(error).__name__,
            error_message=str(error),
            tenant_id=tenant_id,
            user_id=user_id
        )


class BusinessLogger:
    """Logger para eventos de negócio"""
    
    def __init__(self, logger: structlog.BoundLogger = None):
        self.logger = logger or get_logger("business")
    
    def log_trip_created(self, trip_id: int, tenant_id: str, user_id: str):
        """Log de viagem criada"""
        self.logger.info(
            "trip_created",
            trip_id=trip_id,
            tenant_id=tenant_id,
            user_id=user_id
        )
    
    def log_trip_status_changed(self, trip_id: int, old_status: str, new_status: str, tenant_id: str, user_id: str):
        """Log de mudança de status de viagem"""
        self.logger.info(
            "trip_status_changed",
            trip_id=trip_id,
            old_status=old_status,
            new_status=new_status,
            tenant_id=tenant_id,
            user_id=user_id
        )
    
    def log_maintenance_scheduled(self, maintenance_id: int, vehicle_id: int, tenant_id: str, user_id: str):
        """Log de manutenção agendada"""
        self.logger.info(
            "maintenance_scheduled",
            maintenance_id=maintenance_id,
            vehicle_id=vehicle_id,
            tenant_id=tenant_id,
            user_id=user_id
        )
    
    def log_user_login(self, user_id: str, tenant_id: str, success: bool):
        """Log de login de usuário"""
        self.logger.info(
            "user_login",
            user_id=user_id,
            tenant_id=tenant_id,
            success=success
        )


# Inicializar logging
setup_logging()