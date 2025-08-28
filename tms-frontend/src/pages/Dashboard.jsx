import { motion } from 'framer-motion'
import { 
  Users, 
  Truck, 
  Route, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  Calendar,
  MapPin
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

// Dados mockados
const statsData = [
  {
    title: 'Total de Viagens',
    value: '1,234',
    change: '+12%',
    changeType: 'positive',
    icon: Route,
    color: 'bg-blue-500'
  },
  {
    title: 'Clientes Ativos',
    value: '89',
    change: '+5%',
    changeType: 'positive',
    icon: Users,
    color: 'bg-green-500'
  },
  {
    title: 'Veículos Ativos',
    value: '45',
    change: '-2%',
    changeType: 'negative',
    icon: Truck,
    color: 'bg-purple-500'
  },
  {
    title: 'Receita Mensal',
    value: 'R$ 125.000',
    change: '+18%',
    changeType: 'positive',
    icon: DollarSign,
    color: 'bg-orange-500'
  }
]

const revenueData = [
  { name: 'Jan', receita: 4000, custos: 2400 },
  { name: 'Fev', receita: 3000, custos: 1398 },
  { name: 'Mar', receita: 2000, custos: 9800 },
  { name: 'Abr', receita: 2780, custos: 3908 },
  { name: 'Mai', receita: 1890, custos: 4800 },
  { name: 'Jun', receita: 2390, custos: 3800 },
]

const tripStatusData = [
  { name: 'Concluídas', value: 65, color: '#10B981' },
  { name: 'Em Trânsito', value: 25, color: '#3B82F6' },
  { name: 'Pendentes', value: 10, color: '#F59E0B' },
]

const recentTrips = [
  {
    id: 1,
    client: 'Empresa ABC Ltda',
    origin: 'São Paulo, SP',
    destination: 'Rio de Janeiro, RJ',
    status: 'Em Trânsito',
    date: '2024-01-15',
    value: 'R$ 2.500'
  },
  {
    id: 2,
    client: 'Comércio XYZ',
    origin: 'Belo Horizonte, MG',
    destination: 'Brasília, DF',
    status: 'Concluída',
    date: '2024-01-14',
    value: 'R$ 1.800'
  },
  {
    id: 3,
    client: 'Indústria 123',
    origin: 'Curitiba, PR',
    destination: 'Porto Alegre, RS',
    status: 'Pendente',
    date: '2024-01-16',
    value: 'R$ 3.200'
  }
]

export function Dashboard() {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Visão geral do sistema de transporte</p>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsData.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                    <div className="flex items-center mt-2">
                      {stat.changeType === 'positive' ? (
                        <TrendingUp size={16} className="text-green-500 mr-1" />
                      ) : (
                        <TrendingDown size={16} className="text-red-500 mr-1" />
                      )}
                      <span className={`text-sm font-medium ${
                        stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stat.change}
                      </span>
                      <span className="text-sm text-gray-500 ml-1">vs mês anterior</span>
                    </div>
                  </div>
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${stat.color}`}>
                    <stat.icon size={24} className="text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue vs Costs Chart */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Receita vs Custos</CardTitle>
              <CardDescription>Comparativo mensal de receita e custos</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="receita" fill="#3B82F6" name="Receita" />
                  <Bar dataKey="custos" fill="#EF4444" name="Custos" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        {/* Trip Status Chart */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Status das Viagens</CardTitle>
              <CardDescription>Distribuição por status</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={tripStatusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {tripStatusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Recent Trips */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Viagens Recentes</CardTitle>
            <CardDescription>Últimas viagens registradas no sistema</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentTrips.map((trip) => (
                <div key={trip.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                      <Route size={20} className="text-primary-600" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{trip.client}</p>
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <MapPin size={14} />
                        <span>{trip.origin} → {trip.destination}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      trip.status === 'Concluída' ? 'bg-green-100 text-green-800' :
                      trip.status === 'Em Trânsito' ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {trip.status}
                    </div>
                    <p className="text-sm font-medium text-gray-900 mt-1">{trip.value}</p>
                    <p className="text-xs text-gray-500">{trip.date}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}