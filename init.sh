#!/bin/bash

echo "🚛 Iniciando TMS - Transport Management System"
echo "================================================"

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"

# Parar containers existentes (se houver)
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir e iniciar os serviços
echo "🔨 Construindo e iniciando serviços..."
docker-compose up -d --build

# Aguardar um pouco para o banco inicializar
echo "⏳ Aguardando inicialização do banco de dados..."
sleep 10

# Executar setup
echo "🔧 Executando setup do banco..."
./setup.sh

echo ""
echo "🎉 TMS iniciado com sucesso!"
echo ""
echo "📊 Serviços disponíveis:"
echo "   • API FastAPI: http://localhost:8000"
echo "   • Swagger UI:  http://localhost:8000/docs"
echo "   • ReDoc:       http://localhost:8000/redoc"
echo "   • pgAdmin:     http://localhost:5050"
echo ""
echo "🔐 Credenciais padrão:"
echo "   • Admin:       admin / admin123"
echo "   • Operador:    operador / operador123"
echo "   • pgAdmin:     admin@tms.com / admin123"
echo ""
echo "📝 Para ver os logs: docker-compose logs -f app"
echo "🛑 Para parar:       docker-compose down"
echo ""