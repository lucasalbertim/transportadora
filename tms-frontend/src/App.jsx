import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { MainLayout } from './layouts/MainLayout'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { Clients } from './pages/Clients'
import { Drivers } from './pages/Drivers'

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

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    )
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function AppRoutes() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        
        {/* Protected routes */}
        <Route path="/" element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="clients" element={<Clients />} />
          <Route path="drivers" element={<Drivers />} />
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
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
