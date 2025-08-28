from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from models.tenant import Tenant
from models.user import User
import re


def get_tenant_from_header(request: Request) -> Optional[str]:
    """Extrair tenant do header X-Tenant-ID"""
    tenant_id = request.headers.get("X-Tenant-ID")
    if tenant_id:
        return tenant_id
    
    # Fallback para subdomain
    host = request.headers.get("host", "")
    if host:
        # Extrair subdomain (ex: empresa1.tms.com -> empresa1)
        subdomain_match = re.match(r"^([^.]+)\.", host)
        if subdomain_match:
            return subdomain_match.group(1)
    
    return None


def get_tenant_from_path(request: Request) -> Optional[str]:
    """Extrair tenant do path (ex: /api/v1/tenant/empresa1/...)"""
    path = request.url.path
    tenant_match = re.match(r"^/api/v1/tenant/([^/]+)", path)
    if tenant_match:
        return tenant_match.group(1)
    return None


async def get_current_tenant(
    request: Request,
    db: Session = Depends(get_db)
) -> Tenant:
    """Obter tenant atual baseado no header ou path"""
    
    # Tentar obter tenant de diferentes formas
    tenant_id = (
        get_tenant_from_header(request) or
        get_tenant_from_path(request) or
        "default"  # Tenant padrão
    )
    
    # Buscar tenant no banco
    tenant = db.query(Tenant).filter(
        Tenant.slug == tenant_id,
        Tenant.is_active == True
    ).first()
    
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail=f"Tenant '{tenant_id}' não encontrado ou inativo"
        )
    
    # Verificar se está em trial e se expirou
    if tenant.is_trial and tenant.trial_ends_at:
        from datetime import datetime
        if datetime.utcnow() > tenant.trial_ends_at:
            raise HTTPException(
                status_code=402,
                detail="Período de trial expirado. Entre em contato para ativar sua conta."
            )
    
    return tenant


def get_tenant_db_session(tenant: Tenant = Depends(get_current_tenant)):
    """Dependency para obter sessão do banco filtrada por tenant"""
    return tenant


class TenantMiddleware:
    """Middleware para processar tenant em todas as requisições"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Adicionar tenant ao scope para uso posterior
            tenant_id = get_tenant_from_header(request) or get_tenant_from_path(request) or "default"
            scope["tenant_id"] = tenant_id
        
        await self.app(scope, receive, send)