import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clients from './pages/Clients';

// Create a client
const queryClient = new QueryClient();

function App() {
  // Simular autenticação (será integrado com contexto de auth)
  const isAuthenticated = true; // Mudar para false para testar login

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <Routes>
            {/* Rota de login */}
            <Route 
              path="/login" 
              element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} 
            />
            
            {/* Rotas protegidas */}
            <Route 
              path="/" 
              element={isAuthenticated ? <MainLayout /> : <Navigate to="/login" />}
            >
              <Route index element={<Navigate to="/dashboard" />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="clients" element={<Clients />} />
              
              {/* Rotas de cadastros */}
              <Route path="drivers" element={<div className="p-6"><h1 className="text-2xl font-bold">Motoristas</h1><p>Página em desenvolvimento...</p></div>} />
              <Route path="vehicles" element={<div className="p-6"><h1 className="text-2xl font-bold">Veículos</h1><p>Página em desenvolvimento...</p></div>} />
              <Route path="routes" element={<div className="p-6"><h1 className="text-2xl font-bold">Rotas</h1><p>Página em desenvolvimento...</p></div>} />
              
              {/* Rotas de operação */}
              <Route path="trips" element={<div className="p-6"><h1 className="text-2xl font-bold">Viagens</h1><p>Página em desenvolvimento...</p></div>} />
              <Route path="costs" element={<div className="p-6"><h1 className="text-2xl font-bold">Custos</h1><p>Página em desenvolvimento...</p></div>} />
              
              {/* Rotas de manutenção */}
              <Route path="maintenance" element={<div className="p-6"><h1 className="text-2xl font-bold">Manutenção</h1><p>Página em desenvolvimento...</p></div>} />
              
              {/* Rotas de relatórios */}
              <Route path="reports">
                <Route path="financial" element={<div className="p-6"><h1 className="text-2xl font-bold">Relatórios Financeiros</h1><p>Página em desenvolvimento...</p></div>} />
                <Route path="operational" element={<div className="p-6"><h1 className="text-2xl font-bold">Relatórios Operacionais</h1><p>Página em desenvolvimento...</p></div>} />
              </Route>
              
              {/* Rotas de configurações */}
              <Route path="settings">
                <Route path="users" element={<div className="p-6"><h1 className="text-2xl font-bold">Usuários</h1><p>Página em desenvolvimento...</p></div>} />
                <Route path="profile" element={<div className="p-6"><h1 className="text-2xl font-bold">Perfil</h1><p>Página em desenvolvimento...</p></div>} />
              </Route>
            </Route>
            
            {/* Rota 404 */}
            <Route path="*" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
