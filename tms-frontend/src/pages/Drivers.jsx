import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  Search, 
  Plus, 
  Eye, 
  Edit, 
  Trash2, 
  Filter,
  TrendingUp,
  Calendar
} from 'lucide-react'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { driversService } from '../services/api'

export function Drivers() {
  const [drivers, setDrivers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  useEffect(() => {
    loadDrivers()
  }, [])

  const loadDrivers = async () => {
    try {
      setLoading(true)
      const data = await driversService.getAll()
      setDrivers(data)
    } catch (error) {
      console.error('Erro ao carregar motoristas:', error)
      // Usar dados mockados em caso de erro
      setDrivers([
        {
          id: 1,
          name: 'João Silva',
          cnh_number: '12345678901',
          cnh_expiry: '2025-12-31',
          phone: '(11) 99999-9999',
          email: 'joao.silva@email.com',
          status: 'Ativo',
          total_trips: 45,
          total_km: 12500
        },
        {
          id: 2,
          name: 'Maria Santos',
          cnh_number: '98765432109',
          cnh_expiry: '2024-08-15',
          phone: '(21) 88888-8888',
          email: 'maria.santos@email.com',
          status: 'Ativo',
          total_trips: 32,
          total_km: 8900
        },
        {
          id: 3,
          name: 'Pedro Oliveira',
          cnh_number: '11122233344',
          cnh_expiry: '2023-05-20',
          phone: '(31) 77777-7777',
          email: 'pedro.oliveira@email.com',
          status: 'Inativo',
          total_trips: 18,
          total_km: 5200
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const filteredDrivers = drivers.filter(driver => {
    const matchesSearch = driver.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         driver.cnh_number?.includes(searchTerm) ||
                         driver.email?.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesStatus = filterStatus === 'all' || driver.status === filterStatus
    
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: drivers.length,
    active: drivers.filter(d => d.status === 'Ativo').length,
    inactive: drivers.filter(d => d.status === 'Inativo').length,
    totalTrips: drivers.reduce((sum, d) => sum + (d.total_trips || 0), 0)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este motorista?')) {
      try {
        await driversService.delete(id)
        setDrivers(drivers.filter(driver => driver.id !== id))
      } catch (error) {
        console.error('Erro ao excluir motorista:', error)
        alert('Erro ao excluir motorista')
      }
    }
  }

  const isCNHExpired = (expiryDate) => {
    return new Date(expiryDate) < new Date()
  }

  const isCNHExpiringSoon = (expiryDate) => {
    const expiry = new Date(expiryDate)
    const now = new Date()
    const thirtyDaysFromNow = new Date(now.getTime() + (30 * 24 * 60 * 60 * 1000))
    return expiry <= thirtyDaysFromNow && expiry > now
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando motoristas...</p>
        </div>
      </div>
    )
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
          <h1 className="text-3xl font-bold text-gray-900">Motoristas</h1>
          <p className="text-gray-600">Gerencie sua equipe de motoristas</p>
        </div>
        <Button className="flex items-center space-x-2">
          <Plus size={16} />
          <span>Novo Motorista</span>
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
                  <p className="text-sm font-medium text-gray-600">Total de Motoristas</p>
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
                  <p className="text-sm font-medium text-gray-600">Motoristas Ativos</p>
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
                  <p className="text-sm font-medium text-gray-600">Motoristas Inativos</p>
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
                  <p className="text-sm font-medium text-gray-600">Total de Viagens</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalTrips}</p>
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
                  placeholder="Buscar por nome, CNH ou email..."
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

      {/* Drivers Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Lista de Motoristas</CardTitle>
            <CardDescription>
              {filteredDrivers.length} motorista(s) encontrado(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Motorista</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">CNH</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Vencimento CNH</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Contato</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Status</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Viagens</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">KM Rodados</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredDrivers.map((driver, index) => (
                    <motion.tr
                      key={driver.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className="border-b border-gray-100 hover:bg-gray-50"
                    >
                      <td className="py-4 px-4">
                        <div>
                          <p className="font-medium text-gray-900">{driver.name}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-sm text-gray-600">{driver.cnh_number}</td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-2">
                          <Calendar size={14} className="text-gray-500" />
                          <span className={`text-sm ${
                            isCNHExpired(driver.cnh_expiry) ? 'text-red-600 font-medium' :
                            isCNHExpiringSoon(driver.cnh_expiry) ? 'text-yellow-600 font-medium' :
                            'text-gray-600'
                          }`}>
                            {new Date(driver.cnh_expiry).toLocaleDateString('pt-BR')}
                          </span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div>
                          <p className="text-sm text-gray-900">{driver.email}</p>
                          <p className="text-sm text-gray-600">{driver.phone}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          driver.status === 'Ativo' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {driver.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-sm text-gray-900">{driver.total_trips || 0}</td>
                      <td className="py-4 px-4 text-sm text-gray-900">{(driver.total_km || 0).toLocaleString()} km</td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-2">
                          <button className="p-1 text-blue-600 hover:text-blue-800">
                            <Eye size={16} />
                          </button>
                          <button className="p-1 text-gray-600 hover:text-gray-800">
                            <Edit size={16} />
                          </button>
                          <button 
                            className="p-1 text-red-600 hover:text-red-800"
                            onClick={() => handleDelete(driver.id)}
                          >
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