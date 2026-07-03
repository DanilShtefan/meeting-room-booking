import { createContext, useContext, useState, type ReactNode } from 'react'
import client from '../api/client'

interface AuthContextType {
  isAuth: boolean
  login: (login: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuth, setIsAuth] = useState(
    () => localStorage.getItem('access_token') !== null,
  )

  const login = async (login: string, password: string) => {
    const { data } = await client.post('/auth/login', { login, password })
    localStorage.setItem('access_token', data.access_token)
    setIsAuth(true)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setIsAuth(false)
    window.location.href = '/login'
  }

  return (
    <AuthContext.Provider value={{ isAuth, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be inside AuthProvider')
  return ctx
}
