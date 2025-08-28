# 🚛 TMS v3.0 - Multi-tenant Transport Management System

Sistema Multi-tenant de Gerenciamento de Transporte (TMS) versão 3.0 desenvolvido com FastAPI, PostgreSQL, Celery, Redis, Elasticsearch e Docker.

## 🆕 **Novidades da Versão 3.0**

### ✨ **Funcionalidades Multi-tenant (SaaS):**

1. **🏢 Multi-tenant Architecture**
   - Separação completa de dados por transportadora
   - Autenticação por tenant (header X-Tenant-ID ou subdomain)
   - Row Level Security (RLS) implementado
   - Sistema de trial e limites por tenant

2. **📊 Analytics e KPIs Avançados**
   - Taxa de retenção de clientes
   - Taxa de ocupação da frota
   - Custo médio por km rodado
   - Projeção de ganhos futuros
   - Análise de viagens no prazo vs atrasadas
   - Métricas de performance dos motoristas

3. **🔔 Sistema de Notificações**
   - Email via SendGrid
   - WhatsApp via Twilio
   - Alertas automáticos de status de viagens
   - Alertas de manutenção preventiva
   - Alertas de documentos vencendo

4. **📈 Dashboard Executivo Interativo**
   - Gráficos com Plotly/Dash
   - Filtros avançados por período
   - Métricas em tempo real
   - Relatórios customizáveis

5. **🔧 Melhorias Técnicas**
   - Logging estruturado com ELK Stack
   - Monitoramento com Prometheus + Grafana
   - Rate limiting e cache
   - Arquitetura preparada para Kubernetes
   - Testes de integração

### 🛠️ **Stack Tecnológica:**
- **Backend**: FastAPI + SQLAlchemy + Alembic
- **Database**: PostgreSQL com RLS
- **Cache/Queue**: Redis + Celery
- **Logging**: ELK Stack (Elasticsearch + Kibana)
- **Monitoring**: Prometheus + Grafana
- **Notifications**: SendGrid + Twilio
- **Analytics**: Plotly + Dash
- **Container**: Docker Compose + Kubernetes ready

### ✨ **Novas Funcionalidades:**

1. **🔧 Manutenção de Veículos**
   - CRUD completo de manutenções
   - Tipos: Preventiva e Corretiva
   - Relatórios de custos por veículo
   - Controle de status (concluída/pendente)

2. **💰 Gestão Financeira Avançada**
   - Registro de custos reais (combustível, pedágios, diárias, outros)
   - Controle de receita (valor do frete)
   - Cálculo automático de lucratividade
   - Relatórios financeiros detalhados

3. **📊 Relatórios Avançados**
   - Geração em background com Celery
   - Formatos: JSON, Excel, PDF
   - Filtros por cliente, motorista, período
   - Status de progresso em tempo real

4. **📈 Dashboard Melhorado**
   - Gráficos de lucratividade
   - Ranking de clientes mais rentáveis
   - Ranking de motoristas mais eficientes
   - Custos de manutenção vs receita

### 🛠️ **Melhorias Técnicas:**
- **Celery + Redis** para tarefas em background
- **Testes unitários** com pytest
- **Relatórios assíncronos** com progresso
- **Métricas financeiras** avançadas
- **API mais robusta** e escalável

## 🎯 Sobre o Projeto

Este é um MVP de um sistema TMS completo para transportadoras, incluindo:

- **Autenticação JWT** com diferentes níveis de acesso (admin/operador)
- **Cadastros básicos**: Clientes, Motoristas, Veículos e Rotas
- **Gestão de viagens** com controle de status e custos
- **Dashboard** com métricas e estatísticas
- **API REST** documentada com Swagger
- **Banco PostgreSQL** com migrações Alembic
- **Cache Redis** para sessões
- **Docker Compose** para fácil deploy

## 🏗️ Arquitetura

```
TMS/
├── app/
│   ├── core/           # Configurações e utilitários
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   ├── routes/         # Endpoints da API
│   ├── services/       # Lógica de negócio
│   └── utils/          # Utilitários
├── alembic/            # Migrações do banco
├── docker-compose.yml  # Orquestração dos serviços
├── Dockerfile          # Imagem da aplicação
└── requirements.txt    # Dependências Python
```

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Git

### 1. Clone o repositório

```bash
git clone <repository-url>
cd tms
```

### 2. Execute com Docker Compose

```bash
docker compose up -d
```

### 3. Execute o setup do banco

```bash
./setup.sh
```

**Ou execute tudo de uma vez:**

```bash
./init.sh
```

## 📊 Serviços Disponíveis

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| **FastAPI** | 8000 | API principal |
| **PostgreSQL** | 5432 | Banco de dados |
| **Redis** | 6379 | Cache e sessões |
| **pgAdmin** | 5050 | Interface web do PostgreSQL |

## 🔐 Credenciais Padrão

### Usuários do Sistema
- **Admin**: `admin` / `admin123`
- **Operador**: `operador` / `operador123`

### PostgreSQL
- **Host**: `localhost:5432`
- **Database**: `tms_db`
- **User**: `tms_user`
- **Password**: `tms_password`

### pgAdmin
- **URL**: `http://localhost:5050`
- **Email**: `admin@tms.com`
- **Password**: `admin123`

## 📚 Documentação da API

### Swagger UI
Acesse: http://localhost:8000/docs

### ReDoc
Acesse: http://localhost:8000/redoc

## 🔌 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/register` - Cadastrar usuário
- `POST /api/v1/auth/login` - Fazer login
- `GET /api/v1/auth/me` - Dados do usuário logado

### Clientes
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Criar cliente
- `GET /api/v1/clients/{id}` - Buscar cliente
- `PUT /api/v1/clients/{id}` - Atualizar cliente
- `DELETE /api/v1/clients/{id}` - Deletar cliente

### Motoristas
- `GET /api/v1/drivers` - Listar motoristas
- `POST /api/v1/drivers` - Criar motorista
- `GET /api/v1/drivers/{id}` - Buscar motorista
- `PUT /api/v1/drivers/{id}` - Atualizar motorista
- `DELETE /api/v1/drivers/{id}` - Deletar motorista

### Veículos
- `GET /api/v1/vehicles` - Listar veículos
- `POST /api/v1/vehicles` - Criar veículo
- `GET /api/v1/vehicles/{id}` - Buscar veículo
- `PUT /api/v1/vehicles/{id}` - Atualizar veículo
- `DELETE /api/v1/vehicles/{id}` - Deletar veículo

### Rotas
- `GET /api/v1/routes` - Listar rotas
- `POST /api/v1/routes` - Criar rota
- `GET /api/v1/routes/{id}` - Buscar rota
- `PUT /api/v1/routes/{id}` - Atualizar rota
- `DELETE /api/v1/routes/{id}` - Deletar rota

### Viagens
- `GET /api/v1/trips` - Listar viagens
- `POST /api/v1/trips` - Criar viagem
- `GET /api/v1/trips/{id}` - Buscar viagem
- `PUT /api/v1/trips/{id}` - Atualizar viagem
- `PATCH /api/v1/trips/{id}/status` - Atualizar status
- `DELETE /api/v1/trips/{id}` - Deletar viagem

### Dashboard
- `GET /api/v1/dashboard` - Dashboard básico
- `GET /api/v1/reports/dashboard/v2` - Dashboard avançado v2.0

### 🔧 Manutenções (Novo!)
- `GET /api/v1/maintenance` - Listar manutenções
- `POST /api/v1/maintenance` - Criar manutenção
- `GET /api/v1/maintenance/{id}` - Buscar manutenção
- `PUT /api/v1/maintenance/{id}` - Atualizar manutenção
- `DELETE /api/v1/maintenance/{id}` - Deletar manutenção
- `GET /api/v1/maintenance/reports/costs-by-vehicle` - Relatório de custos

### 📊 Relatórios (Novo!)
- `POST /api/v1/reports/generate` - Solicitar relatório
- `GET /api/v1/reports/status/{task_id}` - Verificar status
- `GET /api/v1/dashboard/stats` - Estatísticas gerais

## 🔧 Desenvolvimento

### Estrutura de Dados

#### Usuários
- Email, username, senha, nome completo
- Roles: ADMIN, OPERATOR

#### Clientes
- Nome, CNPJ/CPF, contato, endereço completo

#### Motoristas
- Nome, CNH, vencimento CNH, telefone, endereço

#### Veículos
- Placa, modelo, marca, ano, capacidade, tipo de combustível

#### Rotas
- Nome, origem, destino, distância estimada, tempo estimado

#### Viagens
- Cliente, motorista, veículo, rota
- Datas de saída e chegada
- Status: planned, in_transit, completed, cancelled
- Custos estimados e reais

### Status das Viagens

1. **Planejada** - Viagem criada, aguardando início
2. **Em Trânsito** - Viagem iniciada, em andamento
3. **Concluída** - Viagem finalizada com sucesso
4. **Cancelada** - Viagem cancelada

## 🛠️ Comandos Úteis

### Docker
```bash
# Iniciar serviços
docker compose up -d

# Parar serviços
docker compose down

# Ver logs
docker compose logs -f app

# Executar comando no container
docker compose exec app python -c "print('Hello World')"
```

### Migrações
```bash
# Criar nova migração
docker compose exec app alembic -c alembic.ini revision --autogenerate -m "descrição"

# Aplicar migrações
docker compose exec app alembic -c alembic.ini upgrade head

# Reverter migração
docker compose exec app alembic -c alembic.ini downgrade -1
```

### Seed
```bash
# Popular banco com dados iniciais
docker compose exec app python seed_database.py
```

## 🔒 Segurança

- **JWT Tokens** para autenticação
- **Senhas criptografadas** com bcrypt
- **Controle de acesso** baseado em roles
- **Validação de dados** com Pydantic
- **CORS configurado** para desenvolvimento

## 📈 Dashboard

O dashboard fornece:

- Total de viagens por status
- Contadores de cadastros (clientes, motoristas, veículos, rotas)
- Custos totais estimados vs reais
- Lista das viagens mais recentes

## 🚀 Próximos Passos

- [ ] Interface web (Frontend)
- [ ] Notificações em tempo real
- [ ] Relatórios avançados
- [ ] Integração com GPS
- [ ] Módulo financeiro
- [ ] API para aplicativos móveis

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através dos issues do GitHub.

---

**Desenvolvido com ❤️ para o setor logístico**
