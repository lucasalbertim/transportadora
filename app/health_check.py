#!/usr/bin/env python3
"""
Script de verificação de saúde do TMS
Testa se todos os componentes estão funcionando corretamente
"""

import sys
import os
sys.path.append('/app')

def test_imports():
    """Testar se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from core.database import engine, SessionLocal
        print("✅ core.database - OK")
    except Exception as e:
        print(f"❌ core.database - ERRO: {e}")
        return False
    
    try:
        from models import Base, User, Client, Driver, Vehicle, Route, Trip, Maintenance, MaintenanceType
        print("✅ models - OK")
    except Exception as e:
        print(f"❌ models - ERRO: {e}")
        return False
    
    try:
        from schemas.user import UserCreate, UserLogin
        print("✅ schemas.user - OK")
    except Exception as e:
        print(f"❌ schemas.user - ERRO: {e}")
        return False
    
    try:
        from services.auth import AuthService
        print("✅ services.auth - OK")
    except Exception as e:
        print(f"❌ services.auth - ERRO: {e}")
        return False
    
    try:
        from utils.seed_data import seed_all_data
        print("✅ utils.seed_data - OK")
    except Exception as e:
        print(f"❌ utils.seed_data - ERRO: {e}")
        return False
    
    try:
        from services.maintenance import MaintenanceService
        print("✅ services.maintenance - OK")
    except Exception as e:
        print(f"❌ services.maintenance - ERRO: {e}")
        return False
    
    try:
        from core.celery_app import celery_app
        print("✅ core.celery_app - OK")
    except Exception as e:
        print(f"❌ core.celery_app - ERRO: {e}")
        return False
    
    return True

def test_database_connection():
    """Testar conexão com o banco"""
    print("\n🔍 Testando conexão com banco...")
    
    try:
        from core.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco - OK")
        return True
    except Exception as e:
        print(f"❌ Conexão com banco - ERRO: {e}")
        return False

def test_tables_exist():
    """Testar se as tabelas existem"""
    print("\n🔍 Testando existência das tabelas...")
    
    try:
        from core.database import engine
        from models import Base
        from sqlalchemy import text
        
        # Criar tabelas se não existirem
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas/verificadas - OK")
        
        # Verificar se as tabelas existem
        with engine.connect() as conn:
            tables = ['users', 'clients', 'drivers', 'vehicles', 'routes', 'trips', 'maintenances']
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                print(f"✅ Tabela {table} - OK")
        
        return True
    except Exception as e:
        print(f"❌ Verificação de tabelas - ERRO: {e}")
        return False

def test_seed_data():
    """Testar se o seed funciona"""
    print("\n🔍 Testando seed de dados...")
    
    try:
        from core.database import SessionLocal
        from utils.seed_data import seed_all_data
        
        db = SessionLocal()
        seed_all_data(db)
        db.close()
        print("✅ Seed de dados - OK")
        return True
    except Exception as e:
        print(f"❌ Seed de dados - ERRO: {e}")
        return False

def main():
    """Função principal"""
    print("🚛 Verificação de Saúde do TMS")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_connection,
        test_tables_exist,
        test_seed_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema está funcionando corretamente.")
        return 0
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())