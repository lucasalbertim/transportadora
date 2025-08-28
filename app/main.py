from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.config import settings
from core.database import engine
from models import Base
from routes import auth, clients, drivers, vehicles, routes, trips, dashboard, maintenance, reports, analytics
from core.tenant import TenantMiddleware
from core.logging import RequestLogger, BusinessLogger
import time

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema Multi-tenant de Gerenciamento de Transporte (TMS) - API REST",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware para logging de requisições
request_logger = RequestLogger()
business_logger = BusinessLogger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log da requisição
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    request_logger.log_request(request, tenant_id=tenant_id)
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de resposta
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log da resposta
    request_logger.log_response(request, response, tenant_id=tenant_id)
    
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    request_logger.log_error(request, exc, tenant_id=tenant_id)
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(clients.router, prefix=settings.API_V1_STR)
app.include_router(drivers.router, prefix=settings.API_V1_STR)
app.include_router(vehicles.router, prefix=settings.API_V1_STR)
app.include_router(routes.router, prefix=settings.API_V1_STR)
app.include_router(trips.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(maintenance.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {
        "message": "TMS - Transport Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}