# TMS Frontend - React + Vite + TailwindCSS

Frontend moderno para o sistema TMS (Transport Management System) desenvolvido com React, Vite, TailwindCSS e shadcn/ui.

## 🚀 Tecnologias

- **React 19** - Biblioteca JavaScript para interfaces
- **Vite** - Build tool e dev server
- **TailwindCSS 3** - Framework CSS utilitário
- **shadcn/ui** - Componentes UI modernos
- **Framer Motion** - Animações suaves
- **React Router DOM** - Roteamento
- **React Query** - Gerenciamento de estado e cache
- **Recharts** - Gráficos interativos
- **Lucide React** - Ícones
- **Axios** - Cliente HTTP

## 🎨 Design System

- **Tema**: Azul e branco (profissional e limpo)
- **Tipografia**: Clara e legível
- **Animações**: Suaves com Framer Motion
- **Responsivo**: Desktop, tablet e mobile
- **Acessibilidade**: Componentes acessíveis

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── ui/           # Componentes base (Button, Input, Card, etc.)
│   ├── Sidebar.jsx   # Sidebar retrátil
│   └── Header.jsx    # Header com menu do usuário
├── layouts/
│   └── MainLayout.jsx # Layout principal
├── pages/
│   ├── Login.jsx     # Página de login
│   ├── Dashboard.jsx # Dashboard principal
│   └── Clients.jsx   # Listagem de clientes
├── utils/
│   └── cn.js         # Utilitário para classes CSS
└── App.jsx           # Componente principal com rotas
```

## 🎯 Funcionalidades

### ✅ Implementadas
- **Layout Responsivo**: Sidebar retrátil + header fixo
- **Sistema de Rotas**: Navegação entre páginas
- **Página de Login**: Formulário com validação visual
- **Dashboard**: Cards de estatísticas + gráficos
- **Listagem de Clientes**: Tabela com busca e filtros
- **Componentes UI**: Button, Input, Card, etc.
- **Animações**: Transições suaves entre páginas

### 🔄 Em Desenvolvimento
- **Formulários CRUD**: Criar, editar, excluir registros
- **Integração com API**: Conexão com backend FastAPI
- **Autenticação JWT**: Sistema de login completo
- **Páginas Restantes**: Motoristas, Veículos, Viagens, etc.
- **Relatórios**: Exportação PDF/Excel

## 🚀 Como Executar

### Pré-requisitos
- Node.js 18+ 
- npm ou yarn

### Instalação
```bash
# Navegar para o diretório do frontend
cd tms-frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev
```

### Build para Produção
```bash
# Gerar build otimizado
npm run build

# Preview do build
npm run preview
```

## 📱 Rotas Disponíveis

- `/login` - Página de login
- `/dashboard` - Dashboard principal
- `/clients` - Gerenciamento de clientes
- `/drivers` - Gerenciamento de motoristas
- `/vehicles` - Gerenciamento de veículos
- `/routes` - Gerenciamento de rotas
- `/trips` - Gerenciamento de viagens
- `/costs` - Gerenciamento de custos
- `/maintenance` - Gerenciamento de manutenção
- `/reports/financial` - Relatórios financeiros
- `/reports/operational` - Relatórios operacionais
- `/users` - Gerenciamento de usuários
- `/profile` - Perfil do usuário

## 🎨 Componentes UI

### Button
```jsx
<Button variant="default" size="default">
  Clique aqui
</Button>
```

### Input
```jsx
<Input 
  type="email" 
  placeholder="seu@email.com" 
/>
```

### Card
```jsx
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descrição</CardDescription>
  </CardHeader>
  <CardContent>
    Conteúdo
  </CardContent>
</Card>
```

## 🔧 Configuração

### TailwindCSS
- Configurado com tema personalizado
- Cores primárias em tons de azul
- Variáveis CSS para shadcn/ui

### Vite
- Configuração otimizada para React
- Hot Module Replacement (HMR)
- Build otimizado para produção

### ESLint
- Configuração para React
- Regras de qualidade de código

## 📊 Dados Mockados

O frontend atualmente usa dados mockados para demonstração:
- Clientes com informações completas
- Estatísticas do dashboard
- Gráficos com dados de exemplo
- Viagens recentes

## 🔗 Integração com Backend

### Preparado para:
- **Autenticação JWT**: Headers de autorização
- **API REST**: Endpoints do FastAPI
- **Multi-tenant**: Headers de tenant
- **Upload de arquivos**: Para relatórios
- **WebSocket**: Para atualizações em tempo real

### Exemplo de uso:
```jsx
// Futura integração com API
const { data: clients } = useQuery({
  queryKey: ['clients'],
  queryFn: () => api.get('/clients')
})
```

## 🎯 Próximos Passos

1. **Integração com API**: Conectar com backend FastAPI
2. **Autenticação**: Implementar JWT completo
3. **Formulários**: CRUD completo para todas as entidades
4. **Relatórios**: Exportação PDF/Excel
5. **Notificações**: Sistema de alertas
6. **Testes**: Unit e integration tests
7. **PWA**: Progressive Web App
8. **Mobile**: App nativo ou PWA

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

**TMS Frontend** - Sistema moderno de gerenciamento de transporte 🚛
