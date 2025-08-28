import React from 'react';
import { motion } from 'framer-motion';
import { 
  Truck, 
  Users, 
  Route, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  Calendar,
  MapPin
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const Dashboard = () => {
  // Dados mockados para demonstração
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
      change: '+3%',
      changeType: 'positive',
      icon: Truck,
      color: 'bg-purple-500'
    },
    {
      title: 'Receita Mensal',
      value: 'R$ 125.000',
      change: '+8%',
      changeType: 'positive',
      icon: DollarSign,
      color: 'bg-orange-500'
    }
  ];

  const tripsData = [
    { name: 'Concluídas', value: 85, color: '#10B981' },
    { name: 'Em Trânsito', value: 12, color: '#F59E0B' },
    { name: 'Planejadas', value: 3, color: '#3B82F6' }
  ];

  const revenueData = [
    { month: 'Jan', receita: 95000, custos: 65000 },
    { month: 'Fev', receita: 110000, custos: 70000 },
    { month: 'Mar', receita: 125000, custos: 75000 },
    { month: 'Abr', receita: 135000, custos: 80000 },
    { month: 'Mai', receita: 145000, custos: 85000 },
    { month: 'Jun', receita: 155000, custos: 90000 }
  ];

  const recentTrips = [
    {
      id: 'TRP-001',
      client: 'Empresa ABC',
      origin: 'São Paulo, SP',
      destination: 'Rio de Janeiro, RJ',
      status: 'Em Trânsito',
      date: '2024-01-15'
    },
    {
      id: 'TRP-002',
      client: 'Comércio XYZ',
      origin: 'Belo Horizonte, MG',
      destination: 'São Paulo, SP',
      status: 'Concluída',
      date: '2024-01-14'
    },
    {
      id: 'TRP-003',
      client: 'Indústria DEF',
      origin: 'Rio de Janeiro, RJ',
      destination: 'Belo Horizonte, MG',
      status: 'Planejada',
      date: '2024-01-16'
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Visão geral do sistema de transporte
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsData.map((stat, index) => (
          <motion.div key={stat.title} variants={itemVariants}>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-lg ${stat.color}`}>
                  <stat.icon className="h-4 w-4 text-white" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900">
                  {stat.value}
                </div>
                <div className="flex items-center text-xs text-gray-600 mt-1">
                  {stat.changeType === 'positive' ? (
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                  )}
                  <span className={stat.changeType === 'positive' ? 'text-green-500' : 'text-red-500'}>
                    {stat.change}
                  </span>
                  <span className="ml-1">vs mês anterior</span>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue vs Costs Chart */}
        <motion.div variants={itemVariants}>
          <Card>
            <CardHeader>
              <CardTitle>Receita vs Custos</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="receita" fill="#3B82F6" name="Receita" />
                  <Bar dataKey="custos" fill="#EF4444" name="Custos" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        {/* Trips Status Pie Chart */}
        <motion.div variants={itemVariants}>
          <Card>
            <CardHeader>
              <CardTitle>Status das Viagens</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={tripsData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {tripsData.map((entry, index) => (
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
      <motion.div variants={itemVariants}>
        <Card>
          <CardHeader>
            <CardTitle>Viagens Recentes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentTrips.map((trip) => (
                <div key={trip.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <Route className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{trip.id}</h4>
                      <p className="text-sm text-gray-600">{trip.client}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">
                          {trip.origin} → {trip.destination}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2 mt-1">
                        <Calendar className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">{trip.date}</span>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      trip.status === 'Concluída' ? 'bg-green-100 text-green-800' :
                      trip.status === 'Em Trânsito' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {trip.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  );
};

export default Dashboard;