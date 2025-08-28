import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { MainLayout } from './layouts/MainLayout'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { Clients } from './pages/Clients'

// Create a client
const queryClient = new QueryClient()

// Placeholder components for other pages
const PlaceholderPage = ({ title, description }) => (
  <div className="flex items-center justify-center h-64">
    <div className="text-center">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">{title}</h2>
      <p className="text-gray-600">{description}</p>
    </div>
  </div>
)

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          
          {/* Protected routes */}
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="clients" element={<Clients />} />
            <Route path="drivers" element={<PlaceholderPage title="Motoristas" description="Página de gerenciamento de motoristas" />} />
            <Route path="vehicles" element={<PlaceholderPage title="Veículos" description="Página de gerenciamento de veículos" />} />
            <Route path="routes" element={<PlaceholderPage title="Rotas" description="Página de gerenciamento de rotas" />} />
            <Route path="trips" element={<PlaceholderPage title="Viagens" description="Página de gerenciamento de viagens" />} />
            <Route path="costs" element={<PlaceholderPage title="Custos" description="Página de gerenciamento de custos" />} />
            <Route path="maintenance" element={<PlaceholderPage title="Manutenção" description="Página de gerenciamento de manutenção" />} />
            <Route path="reports">
              <Route path="financial" element={<PlaceholderPage title="Relatórios Financeiros" description="Página de relatórios financeiros" />} />
              <Route path="operational" element={<PlaceholderPage title="Relatórios Operacionais" description="Página de relatórios operacionais" />} />
            </Route>
            <Route path="users" element={<PlaceholderPage title="Usuários" description="Página de gerenciamento de usuários" />} />
            <Route path="profile" element={<PlaceholderPage title="Perfil" description="Página de perfil do usuário" />} />
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  )
}

export default App
