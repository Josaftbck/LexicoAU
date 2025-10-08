import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Components/LOG/Login';
import DashboardApp from './Components/DashboardApp';
import ProtectedRoute from './utils/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import Register from './components/LOG/Register';


function App() {

  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Redirección de "/" a "/login" */}
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Login público */}
          <Route path="/login" element={<Login />} />
          {/* Login público */}
          <Route path="/Register" element={<Register />} />

          {/* Dashboard protegido */}
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                <DashboardApp />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
