import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/LOG/Login';
import Register from './components/LOG/Register';
import DashboardApp from './components/DashboardApp';
import ProtectedRoute from './utils/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import Sidebar from './components/Sidebar'; // ✅ Importamos el nuevo Sidebar
import './components/Sidebar.css'; // ✅ Importamos su CSS

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Redirección inicial */}
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Páginas públicas */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Sección protegida */}
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                {/* ✅ Envolvemos el Dashboard con el Sidebar */}
                <div style={{ display: 'flex', minHeight: '100vh' }}>
                  <Sidebar />
                  <main style={{ flex: 1, padding: '2rem', background: '#f9f9f9' }}>
                    <DashboardApp />
                  </main>
                </div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
