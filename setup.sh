#!/bin/bash

echo "🚛 Setup do TMS - Transport Management System"
echo "=============================================="

# Verificar se o Docker está rodando
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Docker Compose não está rodando. Execute 'docker-compose up -d' primeiro."
    exit 1
fi

echo "✅ Docker Compose está rodando"

# Aguardar o banco estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
until docker-compose exec -T db pg_isready -U tms_user -d tms_db; do
    echo "⏳ Aguardando PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL está pronto!"

# Executar migrações
echo "📊 Executando migrações do banco..."
docker-compose exec -T app alembic -c alembic.ini upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrações executadas com sucesso"
else
    echo "❌ Erro ao executar migrações"
    exit 1
fi

# Executar seed
echo "🌱 Populando banco com dados iniciais..."
docker-compose exec -T app python seed_database.py

if [ $? -eq 0 ]; then
    echo "✅ Seed executado com sucesso"
else
    echo "❌ Erro ao executar seed"
    exit 1
fi

echo ""
echo "🎉 Setup concluído com sucesso!"
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