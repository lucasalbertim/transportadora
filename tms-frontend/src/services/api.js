import axios from 'axios'

// Configuração base da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Adicionar tenant ID (para multi-tenancy)
    const tenantId = localStorage.getItem('tenant_id') || 'default'
    config.headers['X-Tenant-ID'] = tenantId
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado ou inválido
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Serviços de autenticação
export const authService = {
  login: async (username, password) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  register: async (userData) => {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

// Serviços de clientes
export const clientsService = {
  getAll: async (params = {}) => {
    const response = await api.get('/clients', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/clients/${id}`)
    return response.data
  },

  create: async (clientData) => {
    const response = await api.post('/clients', clientData)
    return response.data
  },

  update: async (id, clientData) => {
    const response = await api.put(`/clients/${id}`, clientData)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/clients/${id}`)
    return response.data
  },
}

// Serviços de motoristas
export const driversService = {
  getAll: async (params = {}) => {
    const response = await api.get('/drivers', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/drivers/${id}`)
    return response.data
  },

  create: async (driverData) => {
    const response = await api.post('/drivers', driverData)
    return response.data
  },

  update: async (id, driverData) => {
    const response = await api.put(`/drivers/${id}`, driverData)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/drivers/${id}`)
    return response.data
  },
}

// Serviços de veículos
export const vehiclesService = {
  getAll: async (params = {}) => {
    const response = await api.get('/vehicles', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/vehicles/${id}`)
    return response.data
  },

  create: async (vehicleData) => {
    const response = await api.post('/vehicles', vehicleData)
    return response.data
  },

  update: async (id, vehicleData) => {
    const response = await api.put(`/vehicles/${id}`, vehicleData)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/vehicles/${id}`)
    return response.data
  },
}

// Serviços de rotas
export const routesService = {
  getAll: async (params = {}) => {
    const response = await api.get('/routes', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/routes/${id}`)
    return response.data
  },

  create: async (routeData) => {
    const response = await api.post('/routes', routeData)
    return response.data
  },

  update: async (id, routeData) => {
    const response = await api.put(`/routes/${id}`, routeData)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/routes/${id}`)
    return response.data
  },
}

// Serviços de viagens
export const tripsService = {
  getAll: async (params = {}) => {
    const response = await api.get('/trips', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/trips/${id}`)
    return response.data
  },

  create: async (tripData) => {
    const response = await api.post('/trips', tripData)
    return response.data
  },

  update: async (id, tripData) => {
    const response = await api.put(`/trips/${id}`, tripData)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/trips/${id}`)
    return response.data
  },

  updateStatus: async (id, status) => {
    const response = await api.patch(`/trips/${id}/status`, { status })
    return response.data
  },
}

// Serviços de manutenção
export const maintenanceService = {
  getAll: async (params = {}) => {
    const response = await api.get('/maintenance', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/maintenance/${id}`)
    return response.data
  },

  create: async (maintenanceData) => {
    const response = await api.post('/maintenance', maintenanceData)
    return response.data
  },

  update: async (id, maintenanceData) => {
    const response = await api.put(`/maintenance/${id}`, maintenanceData)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/maintenance/${id}`)
    return response.data
  },
}

// Serviços de dashboard
export const dashboardService = {
  getStats: async () => {
    const response = await api.get('/dashboard/stats')
    return response.data
  },

  getRecentTrips: async () => {
    const response = await api.get('/dashboard/recent-trips')
    return response.data
  },
}

// Serviços de relatórios
export const reportsService = {
  getFinancialReport: async (params = {}) => {
    const response = await api.get('/reports/financial', { params })
    return response.data
  },

  getOperationalReport: async (params = {}) => {
    const response = await api.get('/reports/operational', { params })
    return response.data
  },

  exportPDF: async (reportType, params = {}) => {
    const response = await api.get(`/reports/${reportType}/pdf`, { 
      params,
      responseType: 'blob'
    })
    return response.data
  },

  exportExcel: async (reportType, params = {}) => {
    const response = await api.get(`/reports/${reportType}/excel`, { 
      params,
      responseType: 'blob'
    })
    return response.data
  },
}

// Serviços de analytics
export const analyticsService = {
  getCustomerRetention: async (params = {}) => {
    const response = await api.get('/analytics/customer-retention', { params })
    return response.data
  },

  getFleetOccupation: async (params = {}) => {
    const response = await api.get('/analytics/fleet-occupation', { params })
    return response.data
  },

  getAverageCostPerKm: async (params = {}) => {
    const response = await api.get('/analytics/average-cost-per-km', { params })
    return response.data
  },

  getFutureEarnings: async (params = {}) => {
    const response = await api.get('/analytics/future-earnings', { params })
    return response.data
  },

  getOnTimeDelivery: async (params = {}) => {
    const response = await api.get('/analytics/on-time-delivery', { params })
    return response.data
  },
}

export default api