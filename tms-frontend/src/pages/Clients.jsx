import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  Search, 
  Plus, 
  Eye, 
  Edit, 
  Trash2, 
  Filter,
  TrendingUp
} from 'lucide-react'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'

// Dados mockados
const mockClients = [
  {
    id: 1,
    name: 'Empresa ABC Ltda',
    document: '12.345.678/0001-90',
    email: 'contato@empresaabc.com',
    phone: '(11) 99999-9999',
    city: 'São Paulo, SP',
    status: 'Ativo',
    totalTrips: 45,
    totalRevenue: 'R$ 125.000'
  },
  {
    id: 2,
    name: 'Comércio XYZ',
    document: '98.765.432/0001-10',
    email: 'vendas@comercioxyz.com',
    phone: '(21) 88888-8888',
    city: 'Rio de Janeiro, RJ',
    status: 'Ativo',
    totalTrips: 32,
    totalRevenue: 'R$ 89.500'
  },
  {
    id: 3,
    name: 'Indústria 123',
    document: '11.222.333/0001-44',
    email: 'logistica@industria123.com',
    phone: '(31) 77777-7777',
    city: 'Belo Horizonte, MG',
    status: 'Inativo',
    totalTrips: 18,
    totalRevenue: 'R$ 45.200'
  },
  {
    id: 4,
    name: 'Distribuidora Norte',
    document: '55.666.777/0001-88',
    email: 'pedidos@distribuidoranorte.com',
    phone: '(91) 66666-6666',
    city: 'Belém, PA',
    status: 'Ativo',
    totalTrips: 67,
    totalRevenue: 'R$ 198.300'
  }
]

export function Clients() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  const filteredClients = mockClients.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.document.includes(searchTerm) ||
                         client.email.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesStatus = filterStatus === 'all' || client.status === filterStatus
    
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: mockClients.length,
    active: mockClients.filter(c => c.status === 'Ativo').length,
    inactive: mockClients.filter(c => c.status === 'Inativo').length,
    totalRevenue: mockClients.reduce((sum, c) => sum + parseFloat(c.totalRevenue.replace('R$ ', '').replace('.', '')), 0)
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Clientes</h1>
          <p className="text-gray-600">Gerencie seus clientes e parceiros</p>
        </div>
        <Button className="flex items-center space-x-2">
          <Plus size={16} />
          <span>Novo Cliente</span>
        </Button>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total de Clientes</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                </div>
                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
                  <Users size={24} className="text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Clientes Ativos</p>
                  <p className="text-2xl font-bold text-green-600">{stats.active}</p>
                </div>
                <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                  <TrendingUp size={24} className="text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Clientes Inativos</p>
                  <p className="text-2xl font-bold text-red-600">{stats.inactive}</p>
                </div>
                <div className="w-12 h-12 bg-red-500 rounded-lg flex items-center justify-center">
                  <Users size={24} className="text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Receita Total</p>
                  <p className="text-2xl font-bold text-gray-900">R$ {stats.totalRevenue.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
                  <TrendingUp size={24} className="text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Filters and Search */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.5 }}
      >
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                <Input
                  placeholder="Buscar por nome, documento ou email..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <div className="flex items-center space-x-2">
                <Filter size={16} className="text-gray-500" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="all">Todos os Status</option>
                  <option value="Ativo">Ativo</option>
                  <option value="Inativo">Inativo</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Clients Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Lista de Clientes</CardTitle>
            <CardDescription>
              {filteredClients.length} cliente(s) encontrado(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Cliente</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Documento</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Contato</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Cidade</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Status</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Viagens</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Receita</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredClients.map((client, index) => (
                    <motion.tr
                      key={client.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className="border-b border-gray-100 hover:bg-gray-50"
                    >
                      <td className="py-4 px-4">
                        <div>
                          <p className="font-medium text-gray-900">{client.name}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-sm text-gray-600">{client.document}</td>
                      <td className="py-4 px-4">
                        <div>
                          <p className="text-sm text-gray-900">{client.email}</p>
                          <p className="text-sm text-gray-600">{client.phone}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-sm text-gray-600">{client.city}</td>
                      <td className="py-4 px-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          client.status === 'Ativo' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {client.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-sm text-gray-900">{client.totalTrips}</td>
                      <td className="py-4 px-4 text-sm font-medium text-gray-900">{client.totalRevenue}</td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-2">
                          <button className="p-1 text-blue-600 hover:text-blue-800">
                            <Eye size={16} />
                          </button>
                          <button className="p-1 text-gray-600 hover:text-gray-800">
                            <Edit size={16} />
                          </button>
                          <button className="p-1 text-red-600 hover:text-red-800">
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}