import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Users,
  Truck,
  Route,
  MapPin,
  Settings,
  FileText,
  Wrench,
  ChevronLeft,
  Building2,
  UserCheck,
  BarChart3
} from 'lucide-react';

const menuItems = [
  {
    title: 'Dashboard',
    icon: LayoutDashboard,
    path: '/dashboard',
  },
  {
    title: 'Cadastros',
    icon: Building2,
    children: [
      { title: 'Clientes', icon: Users, path: '/clients' },
      { title: 'Motoristas', icon: UserCheck, path: '/drivers' },
      { title: 'Veículos', icon: Truck, path: '/vehicles' },
      { title: 'Rotas', icon: Route, path: '/routes' },
    ],
  },
  {
    title: 'Operação',
    icon: MapPin,
    children: [
      { title: 'Viagens', icon: Route, path: '/trips' },
      { title: 'Custos', icon: BarChart3, path: '/costs' },
    ],
  },
  {
    title: 'Manutenção',
    icon: Wrench,
    path: '/maintenance',
  },
  {
    title: 'Relatórios',
    icon: FileText,
    children: [
      { title: 'Financeiros', icon: BarChart3, path: '/reports/financial' },
      { title: 'Operacionais', icon: BarChart3, path: '/reports/operational' },
    ],
  },
  {
    title: 'Configurações',
    icon: Settings,
    children: [
      { title: 'Usuários', icon: Users, path: '/settings/users' },
      { title: 'Perfil', icon: UserCheck, path: '/settings/profile' },
    ],
  },
];

const Sidebar = ({ isOpen }) => {
  const [expandedItems, setExpandedItems] = React.useState(new Set());

  const toggleExpanded = (title) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(title)) {
      newExpanded.delete(title);
    } else {
      newExpanded.add(title);
    }
    setExpandedItems(newExpanded);
  };

  const renderMenuItem = (item, level = 0) => {
    const isExpanded = expandedItems.has(item.title);
    const hasChildren = item.children && item.children.length > 0;

    return (
      <div key={item.title}>
        {hasChildren ? (
          <div>
            <button
              onClick={() => toggleExpanded(item.title)}
              className={`w-full flex items-center justify-between px-4 py-2 text-sm font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors ${
                level > 0 ? 'pl-8' : ''
              }`}
            >
              <div className="flex items-center space-x-3">
                <item.icon className="h-5 w-5" />
                {isOpen && <span>{item.title}</span>}
              </div>
              {isOpen && hasChildren && (
                <ChevronLeft
                  className={`h-4 w-4 transition-transform ${
                    isExpanded ? 'rotate-90' : ''
                  }`}
                />
              )}
            </button>
            {isOpen && isExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                {item.children.map((child) => renderMenuItem(child, level + 1))}
              </motion.div>
            )}
          </div>
        ) : (
          <NavLink
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-2 text-sm font-medium transition-colors ${
                level > 0 ? 'pl-8' : ''
              } ${
                isActive
                  ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                  : 'text-gray-700 hover:bg-blue-50 hover:text-blue-600'
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            {isOpen && <span className="ml-3">{item.title}</span>}
          </NavLink>
        )}
      </div>
    );
  };

  return (
    <motion.div
      initial={false}
      animate={{ width: isOpen ? 280 : 70 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="bg-white border-r border-gray-200 flex flex-col"
    >
      {/* Logo */}
      <div className="flex items-center justify-center h-16 border-b border-gray-200">
        {isOpen ? (
          <div className="flex items-center space-x-2">
            <Truck className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">TMS</span>
          </div>
        ) : (
          <Truck className="h-8 w-8 text-blue-600" />
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4">
        <div className="space-y-1">
          {menuItems.map((item) => renderMenuItem(item))}
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        {isOpen && (
          <div className="text-xs text-gray-500 text-center">
            TMS v3.0
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default Sidebar;