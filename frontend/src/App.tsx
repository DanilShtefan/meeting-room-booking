import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuth } = useAuth()
  return isAuth ? <>{children}</> : <Navigate to="/login" replace />
}

function LoginPage() {
  const { login } = useAuth()
  const [loginValue, setLoginValue] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login(loginValue, password)
      window.location.href = '/'
    } catch {
      alert('Invalid credentials')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Login</h1>
      <input
        placeholder="Login"
        value={loginValue}
        onChange={(e) => setLoginValue(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Sign in</button>
    </form>
  )
}

import { useState } from 'react'

function HomePage() {
  const { logout } = useAuth()
  return (
    <div>
      <h1>Meeting Room Booking</h1>
      <button onClick={logout}>Logout</button>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <HomePage />
          </PrivateRoute>
        }
      />
    </Routes>
  )
}

export default App
