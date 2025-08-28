# 🚛 TMS Frontend - Sistema de Transporte

Frontend moderno para o Sistema de Gerenciamento de Transporte (TMS) desenvolvido com React, Vite, TailwindCSS e shadcn/ui.

## 🎨 **Design e Características**

### **Tema e Cores**
- **Cores base**: Branco e tons de azul
- **Azul**: Botões, menus, destaques
- **Branco**: Fundo principal
- **Tipografia**: Clara e legível
- **Estilo**: Dashboard moderno e profissional

### **Layout**
- **Sidebar retrátil** (lado esquerdo) com navegação hierárquica
- **Header fixo** com menu de usuário
- **Área principal** responsiva
- **Animações suaves** com Framer Motion

## 🛠️ **Stack Tecnológica**

- **React 18** - Biblioteca principal
- **Vite** - Build tool e dev server
- **TailwindCSS** - Framework CSS
- **shadcn/ui** - Componentes UI
- **React Router DOM** - Roteamento
- **Framer Motion** - Animações
- **Recharts** - Gráficos interativos
- **Lucide React** - Ícones
- **React Query** - Gerenciamento de estado e cache

## 📁 **Estrutura do Projeto**

```
src/
├── components/
│   ├── ui/           # Componentes base (Button, Input, Card, etc.)
│   ├── Sidebar.jsx   # Sidebar de navegação
│   └── Header.jsx    # Header com menu de usuário
├── pages/
│   ├── Login.jsx     # Página de autenticação
│   ├── Dashboard.jsx # Dashboard principal
│   └── Clients.jsx   # Listagem de clientes
├── layouts/
│   └── MainLayout.jsx # Layout principal
├── hooks/            # Custom hooks
├── services/         # Serviços de API
├── utils/            # Utilitários
├── types/            # Tipos TypeScript
└── contexts/         # Contextos React
```

## 🚀 **Funcionalidades Implementadas**

### ✅ **Autenticação**
- Tela de login responsiva
- Validação de formulários
- Integração preparada para JWT

### ✅ **Dashboard**
- Cards com métricas principais
- Gráficos interativos (Receita vs Custos, Status das Viagens)
- Lista de viagens recentes
- Layout responsivo

### ✅ **Navegação**
- Sidebar retrátil com animação
- Menu hierárquico (Cadastros, Operação, etc.)
- Header com menu de usuário
- Rotas protegidas

### ✅ **Listagens**
- Tabela de clientes com busca e filtros
- Ações CRUD (Visualizar, Editar, Excluir)
- Paginação preparada
- Exportação de dados

### ✅ **Componentes UI**
- Button com variantes
- Input com validação
- Card com header/content/footer
- Sistema de cores consistente

## 🎯 **Rotas Disponíveis**

- `/login` - Autenticação
- `/dashboard` - Dashboard principal
- `/clients` - Gestão de clientes
- `/drivers` - Motoristas (em desenvolvimento)
- `/vehicles` - Veículos (em desenvolvimento)
- `/routes` - Rotas (em desenvolvimento)
- `/trips` - Viagens (em desenvolvimento)
- `/maintenance` - Manutenção (em desenvolvimento)
- `/reports/*` - Relatórios (em desenvolvimento)
- `/settings/*` - Configurações (em desenvolvimento)

## 🚀 **Como Executar**

### **Pré-requisitos**
- Node.js 18+ 
- npm ou yarn

### **Instalação**
```bash
# Clonar o repositório
git clone <repository-url>
cd tms-frontend

# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev
```

### **Build para Produção**
```bash
npm run build
npm run preview
```

## 🔧 **Configuração**

### **Variáveis de Ambiente**
Criar arquivo `.env.local`:
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=TMS Frontend
```

### **Personalização**
- **Cores**: Editar `tailwind.config.js`
- **Componentes**: Modificar `src/components/ui/`
- **Rotas**: Adicionar em `src/App.jsx`

## 📱 **Responsividade**

O sistema é totalmente responsivo:
- **Desktop**: Layout completo com sidebar expandida
- **Tablet**: Sidebar colapsável
- **Mobile**: Menu hambúrguer, layout adaptado

## 🔗 **Integração com Backend**

O frontend está preparado para integração com o backend FastAPI:
- **Autenticação**: JWT tokens
- **API calls**: Axios + React Query
- **Multi-tenant**: Headers X-Tenant-ID
- **Real-time**: WebSocket preparado

## 🎨 **Componentes Disponíveis**

### **UI Components**
- `Button` - Botões com variantes
- `Input` - Campos de entrada
- `Card` - Cards com header/content/footer
- `Modal` - Modais (preparado)
- `Table` - Tabelas (preparado)

### **Layout Components**
- `Sidebar` - Navegação lateral
- `Header` - Cabeçalho
- `MainLayout` - Layout principal

## 📊 **Gráficos e Visualizações**

- **Recharts** para gráficos interativos
- **Bar Chart** - Receita vs Custos
- **Pie Chart** - Status das Viagens
- **Line Chart** - Tendências (preparado)

## 🔮 **Próximos Passos**

1. **Implementar páginas restantes**
2. **Adicionar modais de CRUD**
3. **Integrar com API backend**
4. **Implementar autenticação real**
5. **Adicionar testes**
6. **Otimizar performance**

## 📄 **Licença**

Este projeto faz parte do sistema TMS v3.0 - Multi-tenant SaaS.

---

**Desenvolvido com ❤️ para o Sistema TMS**
