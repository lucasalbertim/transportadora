#!/usr/bin/env python3
"""
Exemplos de uso da API TMS
Execute este script para testar os endpoints da API
"""

import requests
import json
from datetime import datetime, timedelta

# Configuração
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def get_token():
    """Obter token de autenticação"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ Erro ao fazer login: {response.text}")
        return None

def test_auth():
    """Testar autenticação"""
    print("🔐 Testando autenticação...")
    
    token = get_token()
    if token:
        print("✅ Login realizado com sucesso")
        
        # Testar endpoint /me
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuário logado: {user['full_name']} ({user['role']})")
        else:
            print(f"❌ Erro ao obter dados do usuário: {response.text}")
    else:
        print("❌ Falha na autenticação")

def test_clients(token):
    """Testar endpoints de clientes"""
    print("\n👥 Testando endpoints de clientes...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Listar clientes
    response = requests.get(f"{BASE_URL}/clients", headers=headers)
    if response.status_code == 200:
        clients = response.json()
        print(f"✅ Clientes encontrados: {len(clients)}")
        for client in clients[:3]:  # Mostrar apenas os 3 primeiros
            print(f"   • {client['name']} - {client['document']}")
    else:
        print(f"❌ Erro ao listar clientes: {response.text}")

def test_drivers(token):
    """Testar endpoints de motoristas"""
    print("\n🚗 Testando endpoints de motoristas...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Listar motoristas
    response = requests.get(f"{BASE_URL}/drivers", headers=headers)
    if response.status_code == 200:
        drivers = response.json()
        print(f"✅ Motoristas encontrados: {len(drivers)}")
        for driver in drivers[:3]:  # Mostrar apenas os 3 primeiros
            print(f"   • {driver['name']} - CNH: {driver['cnh_number']}")
    else:
        print(f"❌ Erro ao listar motoristas: {response.text}")

def test_vehicles(token):
    """Testar endpoints de veículos"""
    print("\n🚛 Testando endpoints de veículos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Listar veículos
    response = requests.get(f"{BASE_URL}/vehicles", headers=headers)
    if response.status_code == 200:
        vehicles = response.json()
        print(f"✅ Veículos encontrados: {len(vehicles)}")
        for vehicle in vehicles[:3]:  # Mostrar apenas os 3 primeiros
            print(f"   • {vehicle['plate']} - {vehicle['brand']} {vehicle['model']}")
    else:
        print(f"❌ Erro ao listar veículos: {response.text}")

def test_routes(token):
    """Testar endpoints de rotas"""
    print("\n🗺️ Testando endpoints de rotas...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Listar rotas
    response = requests.get(f"{BASE_URL}/routes", headers=headers)
    if response.status_code == 200:
        routes = response.json()
        print(f"✅ Rotas encontradas: {len(routes)}")
        for route in routes[:3]:  # Mostrar apenas as 3 primeiras
            print(f"   • {route['name']} - {route['origin']} → {route['destination']}")
    else:
        print(f"❌ Erro ao listar rotas: {response.text}")

def test_trips(token):
    """Testar endpoints de viagens"""
    print("\n🚚 Testando endpoints de viagens...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Listar viagens
    response = requests.get(f"{BASE_URL}/trips", headers=headers)
    if response.status_code == 200:
        trips = response.json()
        print(f"✅ Viagens encontradas: {len(trips)}")
        for trip in trips[:3]:  # Mostrar apenas as 3 primeiras
            print(f"   • Viagem {trip['id']}: {trip['client_name']} → {trip['driver_name']} ({trip['status']})")
    else:
        print(f"❌ Erro ao listar viagens: {response.text}")

def test_dashboard(token):
    """Testar dashboard"""
    print("\n📊 Testando dashboard...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obter estatísticas
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print("✅ Dashboard carregado:")
        print(f"   • Total de viagens: {stats['total_trips']}")
        print(f"   • Viagens planejadas: {stats['planned_trips']}")
        print(f"   • Viagens em trânsito: {stats['in_transit_trips']}")
        print(f"   • Viagens concluídas: {stats['completed_trips']}")
        print(f"   • Total de clientes: {stats['total_clients']}")
        print(f"   • Total de motoristas: {stats['total_drivers']}")
        print(f"   • Total de veículos: {stats['total_vehicles']}")
        print(f"   • Custos estimados: R$ {stats['total_estimated_costs']:.2f}")
    else:
        print(f"❌ Erro ao carregar dashboard: {response.text}")

def create_sample_trip(token):
    """Criar uma viagem de exemplo"""
    print("\n➕ Criando viagem de exemplo...")
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Primeiro, vamos buscar IDs existentes
    clients_response = requests.get(f"{BASE_URL}/clients", headers=headers)
    drivers_response = requests.get(f"{BASE_URL}/drivers", headers=headers)
    vehicles_response = requests.get(f"{BASE_URL}/vehicles", headers=headers)
    routes_response = requests.get(f"{BASE_URL}/routes", headers=headers)
    
    if all(r.status_code == 200 for r in [clients_response, drivers_response, vehicles_response, routes_response]):
        clients = clients_response.json()
        drivers = drivers_response.json()
        vehicles = vehicles_response.json()
        routes = routes_response.json()
        
        if clients and drivers and vehicles and routes:
            # Criar viagem
            trip_data = {
                "client_id": clients[0]["id"],
                "driver_id": drivers[0]["id"],
                "vehicle_id": vehicles[0]["id"],
                "route_id": routes[0]["id"],
                "departure_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "estimated_arrival": (datetime.now() + timedelta(days=1, hours=6)).isoformat(),
                "estimated_fuel_cost": 500.0,
                "estimated_toll_cost": 150.0,
                "notes": "Viagem de exemplo criada via API"
            }
            
            response = requests.post(f"{BASE_URL}/trips", headers=headers, json=trip_data)
            if response.status_code == 200:
                trip = response.json()
                print(f"✅ Viagem criada com sucesso! ID: {trip['id']}")
                return trip["id"]
            else:
                print(f"❌ Erro ao criar viagem: {response.text}")
        else:
            print("❌ Dados insuficientes para criar viagem")
    else:
        print("❌ Erro ao buscar dados para criar viagem")
    
    return None

def main():
    """Função principal"""
    print("🚛 Testando API TMS")
    print("=" * 50)
    
    # Testar autenticação
    token = get_token()
    if not token:
        print("❌ Não foi possível obter token. Verifique se a API está rodando.")
        return
    
    # Testar endpoints
    test_auth()
    test_clients(token)
    test_drivers(token)
    test_vehicles(token)
    test_routes(token)
    test_trips(token)
    test_dashboard(token)
    
    # Criar viagem de exemplo
    trip_id = create_sample_trip(token)
    
    print("\n" + "=" * 50)
    print("🎉 Testes concluídos!")
    print(f"📚 Documentação: http://localhost:8000/docs")
    print(f"📊 Dashboard: http://localhost:8000/api/v1/dashboard/stats")

if __name__ == "__main__":
    main()