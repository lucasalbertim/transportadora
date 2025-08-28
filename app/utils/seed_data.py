from sqlalchemy.orm import Session
from core.security import get_password_hash
from models.user import User, UserRole
from models.tenant import Tenant
from models.client import Client
from models.driver import Driver
from models.vehicle import Vehicle
from models.route import Route
from models.maintenance import Maintenance, MaintenanceType
from datetime import date, datetime, timedelta


def seed_tenants(db: Session):
    """Criar tenants iniciais"""
    if db.query(Tenant).count() > 0:
        return
    
    # Tenant padrão
    default_tenant = Tenant(
        name="Transportadora Padrão",
        slug="default",
        company_name="Transportadora Padrão Ltda",
        cnpj="12.345.678/0001-90",
        address="Rua das Transportadoras, 123",
        phone="(11) 99999-9999",
        email="contato@transportadorapadrao.com",
        max_users=50,
        max_vehicles=100,
        is_trial=False
    )
    
    # Tenant de exemplo
    example_tenant = Tenant(
        name="Logística Express",
        slug="logistica-express",
        company_name="Logística Express Ltda",
        cnpj="98.765.432/0001-10",
        address="Av. Logística, 456",
        phone="(21) 88888-8888",
        email="contato@logisticaexpress.com",
        max_users=20,
        max_vehicles=50,
        is_trial=True,
        trial_ends_at=datetime.now() + timedelta(days=30)
    )
    
    db.add(default_tenant)
    db.add(example_tenant)
    db.commit()
    
    return default_tenant, example_tenant


def seed_users(db: Session):
    """Criar usuários iniciais"""
    # Verificar se já existem usuários
    if db.query(User).count() > 0:
        return
    
    # Buscar tenants
    default_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
    if not default_tenant:
        return
    
    # Admin
    admin_user = User(
        tenant_id=default_tenant.id,
        email="admin@tms.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        full_name="Administrador do Sistema",
        role=UserRole.ADMIN
    )
    
    # Operador
    operator_user = User(
        tenant_id=default_tenant.id,
        email="operador@tms.com",
        username="operador",
        hashed_password=get_password_hash("operador123"),
        full_name="Operador do Sistema",
        role=UserRole.OPERATOR
    )
    
    db.add(admin_user)
    db.add(operator_user)
    db.commit()


def seed_clients(db: Session):
    """Criar clientes iniciais"""
    if db.query(Client).count() > 0:
        return
    
    clients = [
        Client(
            name="Empresa ABC Ltda",
            document="12.345.678/0001-90",
            contact_name="João Silva",
            phone="(11) 99999-9999",
            email="contato@empresaabc.com",
            address="Rua das Flores, 123",
            city="São Paulo",
            state="SP",
            zip_code="01234-567"
        ),
        Client(
            name="Comércio XYZ",
            document="98.765.432/0001-10",
            contact_name="Maria Santos",
            phone="(21) 88888-8888",
            email="vendas@comercioxyz.com",
            address="Av. Principal, 456",
            city="Rio de Janeiro",
            state="RJ",
            zip_code="20000-000"
        ),
        Client(
            name="Indústria DEF",
            document="11.222.333/0001-44",
            contact_name="Pedro Costa",
            phone="(31) 77777-7777",
            email="pedido@industriadef.com",
            address="Rua Industrial, 789",
            city="Belo Horizonte",
            state="MG",
            zip_code="30000-000"
        )
    ]
    
    for client in clients:
        db.add(client)
    db.commit()


def seed_drivers(db: Session):
    """Criar motoristas iniciais"""
    if db.query(Driver).count() > 0:
        return
    
    drivers = [
        Driver(
            name="Carlos Oliveira",
            cnh_number="12345678901",
            cnh_expiry=date(2025, 12, 31),
            phone="(11) 96666-6666",
            email="carlos.oliveira@email.com",
            address="Rua dos Motoristas, 100",
            is_active=True
        ),
        Driver(
            name="Roberto Santos",
            cnh_number="98765432109",
            cnh_expiry=date(2024, 6, 30),
            phone="(21) 95555-5555",
            email="roberto.santos@email.com",
            address="Av. dos Condutores, 200",
            is_active=True
        ),
        Driver(
            name="Fernando Lima",
            cnh_number="11122233344",
            cnh_expiry=date(2026, 3, 15),
            phone="(31) 94444-4444",
            email="fernando.lima@email.com",
            address="Rua dos Caminhoneiros, 300",
            is_active=True
        )
    ]
    
    for driver in drivers:
        db.add(driver)
    db.commit()


def seed_vehicles(db: Session):
    """Criar veículos iniciais"""
    if db.query(Vehicle).count() > 0:
        return
    
    vehicles = [
        Vehicle(
            plate="ABC-1234",
            model="FH 460",
            brand="Volvo",
            year=2020,
            capacity=25.0,
            fuel_type="Diesel",
            is_active=True
        ),
        Vehicle(
            plate="XYZ-5678",
            model="Actros 2651",
            brand="Mercedes-Benz",
            year=2021,
            capacity=30.0,
            fuel_type="Diesel",
            is_active=True
        ),
        Vehicle(
            plate="DEF-9012",
            model="Truck 2428",
            brand="Scania",
            year=2019,
            capacity=20.0,
            fuel_type="Diesel",
            is_active=True
        )
    ]
    
    for vehicle in vehicles:
        db.add(vehicle)
    db.commit()


def seed_routes(db: Session):
    """Criar rotas iniciais"""
    if db.query(Route).count() > 0:
        return
    
    routes = [
        Route(
            name="São Paulo - Rio de Janeiro",
            origin="São Paulo, SP",
            destination="Rio de Janeiro, RJ",
            estimated_distance=430.0,
            estimated_time=6.0,
            description="Rota principal entre SP e RJ",
            is_active=True
        ),
        Route(
            name="São Paulo - Belo Horizonte",
            origin="São Paulo, SP",
            destination="Belo Horizonte, MG",
            estimated_distance=580.0,
            estimated_time=8.0,
            description="Rota para MG",
            is_active=True
        ),
        Route(
            name="Rio de Janeiro - Belo Horizonte",
            origin="Rio de Janeiro, RJ",
            destination="Belo Horizonte, MG",
            estimated_distance=440.0,
            estimated_time=6.5,
            description="Rota RJ-MG",
            is_active=True
        )
    ]
    
    for route in routes:
        db.add(route)
    db.commit()


def seed_maintenances(db: Session):
    """Criar manutenções iniciais"""
    if db.query(Maintenance).count() > 0:
        return
    
    # Buscar veículos existentes
    vehicles = db.query(Vehicle).all()
    if not vehicles:
        return
    
    maintenances = [
        Maintenance(
            vehicle_id=vehicles[0].id,
            maintenance_type=MaintenanceType.PREVENTIVE,
            maintenance_date=date(2024, 1, 15),
            cost=1500.00,
            description="Troca de óleo e filtros",
            observations="Manutenção preventiva realizada conforme cronograma",
            is_completed=True
        ),
        Maintenance(
            vehicle_id=vehicles[0].id,
            maintenance_type=MaintenanceType.CORRECTIVE,
            maintenance_date=date(2024, 2, 10),
            cost=2500.00,
            description="Reparo no sistema de freios",
            observations="Problema identificado durante inspeção",
            is_completed=True
        ),
        Maintenance(
            vehicle_id=vehicles[1].id if len(vehicles) > 1 else vehicles[0].id,
            maintenance_type=MaintenanceType.PREVENTIVE,
            maintenance_date=date(2024, 1, 20),
            cost=1200.00,
            description="Revisão geral e alinhamento",
            observations="Veículo em bom estado geral",
            is_completed=True
        ),
        Maintenance(
            vehicle_id=vehicles[1].id if len(vehicles) > 1 else vehicles[0].id,
            maintenance_type=MaintenanceType.PREVENTIVE,
            maintenance_date=date(2024, 3, 5),
            cost=800.00,
            description="Troca de pneus",
            observations="Pneus desgastados, troca preventiva",
            is_completed=False
        )
    ]
    
    for maintenance in maintenances:
        db.add(maintenance)
    db.commit()


def seed_all_data(db: Session):
    """Executar todos os seeds"""
    print("🌱 Iniciando seed dos dados...")
    
    seed_tenants(db)
    print("✅ Tenants criados")
    
    seed_users(db)
    print("✅ Usuários criados")
    
    seed_clients(db)
    print("✅ Clientes criados")
    
    seed_drivers(db)
    print("✅ Motoristas criados")
    
    seed_vehicles(db)
    print("✅ Veículos criados")
    
    seed_routes(db)
    print("✅ Rotas criadas")
    
    seed_maintenances(db)
    print("✅ Manutenções criadas")
    
    print("🎉 Seed concluído com sucesso!")