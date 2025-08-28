# 🚛 TMS v3.0 - Sistema Multi-tenant de Transporte Completo

Sistema completo de Gerenciamento de Transporte (TMS) versão 3.0 com **Backend FastAPI** e **Frontend React**, desenvolvido como uma solução SaaS multi-tenant.

## 🏗️ **Arquitetura Completa**

```
📦 TMS v3.0 - Sistema Completo
├── 🐍 Backend (FastAPI + PostgreSQL)
│   ├── app/                    # Código principal do backend
│   ├── docker-compose.yml      # Orquestração de containers
│   ├── Dockerfile              # Container do backend
│   └── requirements.txt        # Dependências Python
├── ⚛️ Frontend (React + Vite)
│   ├── tms-frontend/           # Código do frontend
│   ├── src/                    # Código fonte React
│   └── package.json            # Dependências Node.js
└── 📚 Documentação
    ├── README.md               # Este arquivo
    └── examples/               # Exemplos de uso
```

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
   - Análise de viagens atrasadas vs. no prazo

3. **🔔 Sistema de Notificações**
   - Email via SendGrid
   - WhatsApp via Twilio
   - Alertas automáticos de status de viagens
   - Alertas de manutenção preventiva

4. **📈 Dashboard Executivo Interativo**
   - Gráficos com Plotly/Dash
   - Filtros avançados por período
   - Métricas em tempo real
   - Relatórios customizáveis

5. **🎨 Frontend Moderno**
   - React + Vite + TailwindCSS
   - Interface responsiva e moderna
   - Sidebar retrátil com navegação
   - Gráficos interativos com Recharts

### 🛠️ **Stack Tecnológica Completa:**

#### **Backend:**
- **FastAPI** - API REST moderna
- **PostgreSQL** - Banco de dados principal
- **SQLAlchemy** - ORM avançado
- **Redis** - Cache e filas
- **Celery** - Tarefas em background
- **JWT** - Autenticação segura

#### **Frontend:**
- **React 18** - Biblioteca principal
- **Vite** - Build tool e dev server
- **TailwindCSS** - Framework CSS
- **shadcn/ui** - Componentes UI
- **Framer Motion** - Animações
- **Recharts** - Gráficos interativos

#### **Infraestrutura:**
- **Docker Compose** - Orquestração
- **ELK Stack** - Logging estruturado
- **Prometheus + Grafana** - Monitoramento
- **Kubernetes Ready** - Escalabilidade

## 🚀 **Como Executar o Sistema Completo**

### **Opção 1: Backend + Frontend Separados**

#### **Backend (FastAPI):**
```bash
# Clonar o repositório
git clone <repository-url>
cd tms-backend

# Executar com Docker
./init.sh

# Acessar API
http://localhost:8000/docs
```

#### **Frontend (React):**
```bash
# Navegar para o frontend
cd tms-frontend

# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Acessar interface
http://localhost:5173
```

### **Opção 2: Docker Compose Completo (Recomendado)**

```bash
# Executar todo o sistema
docker-compose up -d

# Acessar serviços:
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# Kibana: http://localhost:5601
```

## 📁 **Estrutura Detalhada do Projeto**

### **Backend (`/app/`)**
```
app/
├── core/                    # Configurações e utilitários
│   ├── config.py           # Configurações da aplicação
│   ├── database.py         # Conexão com banco
│   ├── security.py         # Autenticação JWT
│   ├── tenant.py           # Sistema multi-tenant
│   └── logging.py          # Logging estruturado
├── models/                  # Modelos SQLAlchemy
│   ├── tenant.py           # Modelo de tenant
│   ├── user.py             # Usuários
│   ├── client.py           # Clientes
│   ├── driver.py           # Motoristas
│   ├── vehicle.py          # Veículos
│   ├── route.py            # Rotas
│   ├── trip.py             # Viagens
│   └── maintenance.py      # Manutenções
├── schemas/                 # Schemas Pydantic
├── services/                # Lógica de negócio
├── routes/                  # Endpoints da API
├── tasks/                   # Tarefas Celery
└── utils/                   # Utilitários
```

### **Frontend (`/tms-frontend/`)**
```
tms-frontend/
├── src/
│   ├── components/          # Componentes React
│   │   ├── ui/             # Componentes base (shadcn/ui)
│   │   ├── Sidebar.jsx     # Navegação lateral
│   │   └── Header.jsx      # Cabeçalho
│   ├── pages/              # Páginas da aplicação
│   │   ├── Login.jsx       # Autenticação
│   │   ├── Dashboard.jsx   # Dashboard principal
│   │   └── Clients.jsx     # Gestão de clientes
│   ├── layouts/            # Layouts
│   ├── hooks/              # Custom hooks
│   ├── services/           # Serviços de API
│   └── utils/              # Utilitários
├── public/                 # Arquivos estáticos
└── package.json            # Dependências
```

## 🎯 **Funcionalidades por Módulo**

### **🔐 Autenticação e Usuários**
- ✅ Login/Logout com JWT
- ✅ Controle de permissões (admin/operador)
- ✅ Sistema multi-tenant
- ✅ Interface de login responsiva

### **📋 Cadastros Básicos**
- ✅ **Clientes**: CRUD completo com interface
- ✅ **Motoristas**: CRUD completo
- ✅ **Veículos**: CRUD completo
- ✅ **Rotas**: CRUD completo

### **🚛 Operação**
- ✅ **Viagens**: Registro e acompanhamento
- ✅ **Custos**: Gestão financeira
- ✅ **Status**: Atualização em tempo real
- ✅ **Dashboard**: Visão geral operacional

### **🔧 Manutenção**
- ✅ **Veículos**: Agendamento e controle
- ✅ **Alertas**: Notificações automáticas
- ✅ **Relatórios**: Custos por veículo

### **📊 Relatórios e Analytics**
- ✅ **Financeiros**: Receita vs Custos
- ✅ **Operacionais**: KPIs de performance
- ✅ **Gráficos**: Interativos e responsivos
- ✅ **Exportação**: PDF/Excel

### **⚙️ Configurações**
- ✅ **Usuários**: Gestão de acessos
- ✅ **Perfil**: Configurações pessoais
- ✅ **Tenant**: Configurações da empresa

## 🔗 **Integração Backend ↔ Frontend**

### **API Endpoints Principais:**
```
POST   /api/v1/auth/login          # Autenticação
GET    /api/v1/dashboard           # Dashboard
GET    /api/v1/clients             # Listar clientes
POST   /api/v1/clients             # Criar cliente
PUT    /api/v1/clients/{id}        # Atualizar cliente
DELETE /api/v1/clients/{id}        # Deletar cliente
GET    /api/v1/analytics/*         # Analytics e KPIs
```

### **Headers de Autenticação:**
```javascript
// Frontend envia:
{
  'Authorization': 'Bearer <jwt_token>',
  'X-Tenant-ID': 'tenant_slug'
}
```

## 📊 **Serviços Disponíveis**

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| **FastAPI** | 8000 | API principal |
| **React Frontend** | 5173 | Interface web |
| **PostgreSQL** | 5432 | Banco de dados |
| **Redis** | 6379 | Cache e filas |
| **Celery** | - | Worker de tarefas |
| **Elasticsearch** | 9200 | Logs estruturados |
| **Kibana** | 5601 | Visualização de logs |
| **Prometheus** | 9090 | Métricas |
| **Grafana** | 3000 | Dashboards |
| **pgAdmin** | 5050 | Interface PostgreSQL |

## 🚀 **Deploy e Produção**

### **Desenvolvimento:**
```bash
# Backend
./init.sh

# Frontend
cd tms-frontend && npm run dev
```

### **Produção:**
```bash
# Build completo
docker-compose -f docker-compose.prod.yml up -d

# Ou Kubernetes
kubectl apply -f k8s/
```

## 📈 **Monitoramento e Observabilidade**

- **Logs**: ELK Stack (Elasticsearch + Kibana)
- **Métricas**: Prometheus + Grafana
- **Tracing**: Preparado para Jaeger
- **Health Checks**: Endpoints de saúde

## 🔮 **Roadmap Futuro**

### **v3.1 - Melhorias**
- [ ] App mobile para motoristas
- [ ] Integração com ERPs
- [ ] Machine Learning para predições
- [ ] WebSocket para real-time

### **v3.2 - Escalabilidade**
- [ ] Kubernetes deployment
- [ ] Microserviços
- [ ] API Gateway
- [ ] Service Mesh

### **v3.3 - Inteligência**
- [ ] IA para otimização de rotas
- [ ] Predição de demandas
- [ ] Análise preditiva
- [ ] Chatbot integrado

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 **Licença**

Este projeto é parte do sistema TMS v3.0 - Multi-tenant SaaS.

## 📞 **Suporte**

- **Documentação**: `/docs`
- **API Docs**: `http://localhost:8000/docs`
- **Issues**: GitHub Issues
- **Email**: suporte@tms.com

---

## 🎉 **Status do Projeto**

### ✅ **Completo:**
- Backend FastAPI com multi-tenant
- Frontend React moderno
- Sistema de autenticação
- Dashboard interativo
- CRUD completo
- Analytics avançados
- Notificações
- Monitoramento

### 🚀 **Pronto para Produção:**
- Docker Compose configurado
- Logging estruturado
- Métricas e monitoramento
- Documentação completa
- Testes preparados

**O TMS v3.0 está completo e pronto para uso em produção! 🎉**

---

**Desenvolvido com ❤️ para o setor de transporte**
