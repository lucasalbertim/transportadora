#!/bin/bash

# Script para aguardar o banco de dados estar pronto
echo "🔍 Aguardando PostgreSQL estar pronto..."

until pg_isready -h db -p 5432 -U tms_user -d tms_db; do
    echo "⏳ PostgreSQL ainda não está pronto..."
    sleep 2
done

echo "✅ PostgreSQL está pronto!"

# Executar migrações
echo "📊 Executando migrações..."
alembic upgrade head

# Executar seed
echo "🌱 Populando banco com dados iniciais..."
python seed_database.py

echo "🎉 Setup concluído!"