import { NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  LayoutDashboard, 
  Users, 
  Truck, 
  Route, 
  MapPin, 
  Wrench, 
  FileText, 
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { useState } from 'react'

const menuItems = [
  {
    title: 'Dashboard',
    icon: LayoutDashboard,
    path: '/dashboard'
  },
  {
    title: 'Cadastros',
    icon: Users,
    children: [
      { title: 'Clientes', path: '/clients' },
      { title: 'Motoristas', path: '/drivers' },
      { title: 'Veículos', path: '/vehicles' },
      { title: 'Rotas', path: '/routes' }
    ]
  },
  {
    title: 'Operação',
    icon: Truck,
    children: [
      { title: 'Viagens', path: '/trips' },
      { title: 'Custos', path: '/costs' }
    ]
  },
  {
    title: 'Manutenção',
    icon: Wrench,
    path: '/maintenance'
  },
  {
    title: 'Relatórios',
    icon: FileText,
    children: [
      { title: 'Financeiros', path: '/reports/financial' },
      { title: 'Operacionais', path: '/reports/operational' }
    ]
  },
  {
    title: 'Configurações',
    icon: Settings,
    children: [
      { title: 'Usuários', path: '/users' },
      { title: 'Perfil', path: '/profile' }
    ]
  }
]

export function Sidebar({ open, onToggle }) {
  return (
    <motion.div
      initial={false}
      animate={{ width: open ? 280 : 70 }}
      className="bg-white border-r border-gray-200 flex flex-col"
    >
      {/* Logo */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-xl font-bold text-primary-600"
          >
            TMS
          </motion.div>
        )}
        <button
          onClick={onToggle}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          {open ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
        </button>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item, index) => (
          <MenuItem key={index} item={item} open={open} />
        ))}
      </nav>
    </motion.div>
  )
}

function MenuItem({ item, open }) {
  const [expanded, setExpanded] = useState(false)
  const hasChildren = item.children && item.children.length > 0

  if (hasChildren) {
    return (
      <div>
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full flex items-center justify-between p-3 rounded-lg hover:bg-gray-100 transition-colors text-left"
        >
          <div className="flex items-center space-x-3">
            <item.icon size={20} className="text-gray-600" />
            {open && <span className="text-sm font-medium">{item.title}</span>}
          </div>
          {open && (
            <motion.div
              animate={{ rotate: expanded ? 90 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronRight size={16} />
            </motion.div>
          )}
        </button>
        
        {open && (
          <motion.div
            initial={false}
            animate={{ height: expanded ? 'auto' : 0, opacity: expanded ? 1 : 0 }}
            className="overflow-hidden"
          >
            <div className="ml-8 mt-2 space-y-1">
              {item.children.map((child, childIndex) => (
                <NavLink
                  key={childIndex}
                  to={child.path}
                  className={({ isActive }) =>
                    `block p-2 rounded-lg text-sm transition-colors ${
                      isActive 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-600 hover:bg-gray-100'
                    }`
                  }
                >
                  {child.title}
                </NavLink>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    )
  }

  return (
    <NavLink
      to={item.path}
      className={({ isActive }) =>
        `flex items-center space-x-3 p-3 rounded-lg transition-colors ${
          isActive 
            ? 'bg-primary-100 text-primary-700' 
            : 'text-gray-600 hover:bg-gray-100'
        }`
      }
    >
      <item.icon size={20} />
      {open && <span className="text-sm font-medium">{item.title}</span>}
    </NavLink>
  )
}