import { useState } from 'react'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Truck } from 'lucide-react'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'

export function Login() {
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    // Simular login
    setTimeout(() => {
      setLoading(false)
      // Aqui seria a integração com a API
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Card className="shadow-xl">
          <CardHeader className="text-center">
            <div className="mx-auto w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mb-4">
              <Truck size={32} className="text-white" />
            </div>
            <CardTitle className="text-2xl">TMS Login</CardTitle>
            <CardDescription>
              Entre com suas credenciais para acessar o sistema
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                  Senha
                </label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>
              
              <Button
                type="submit"
                className="w-full"
                disabled={loading}
              >
                {loading ? 'Entrando...' : 'Entrar'}
              </Button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Esqueceu sua senha?{' '}
                <a href="#" className="text-primary-600 hover:text-primary-700 font-medium">
                  Recuperar senha
                </a>
              </p>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}