import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import axios from 'axios';
import './Login.css';
import { FaUser, FaLock, FaSignInAlt } from 'react-icons/fa';
import logo from "../../assets/lexion_icon.png"; // 🌀 tu nuevo logo

function Login() {
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // 🔹 Llamada a tu API FastAPI
      const response = await axios.post('http://localhost:8000/login', {
        usuario,
        password,
      });

      // 🔹 Guardar token y datos del usuario
      login({
        token: response.data.access_token,
        user: {
          id: response.data.usuario_id,
          usuario: response.data.usuario,
          nombre: response.data.nombre_completo,
          email: response.data.email,
        },
      });

      // 🔹 Redirigir al dashboard o ruta anterior
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    } catch (err) {
      console.error('Error de login:', err);
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        err.response?.data?.error ||
        '❌ No se pudo iniciar sesión. Verifica tus credenciales.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card shadow">
 
          {/* 🔹 Logo y título */}
          <div className="login-header">
            <img src={logo} alt="Lexion Logo" className="login-logo" />
            <h1 className="login-title">Lexion</h1>
            <p className="login-subtitle">Enter your intelligent workspace</p>
          </div>
        <div className="login-body">
          {error && (
            <div className="alert alert-danger text-center py-2 error-message">
              {error}
            </div>
          )}

          <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label className="form-label fw-semibold">
                <FaUser className="me-2" /> Usuario
              </label>
              <input
                type="text"
                className="form-control"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
                required
                placeholder="Ingresa tu usuario"
              />
            </div>

            <div className="form-group mb-4">
              <label className="form-label fw-semibold">
                <FaLock className="me-2" /> Contraseña
              </label>
              <input
                type="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Ingresa tu contraseña"
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary login-btn w-100"
              disabled={isLoading}
            >
              {isLoading ? (
                <span>Cargando...</span>
              ) : (
                <>
                  <FaSignInAlt className="me-2" /> Ingresar
                </>
              )}
            </button>
          </form>
        </div>

        <div className="login-footer text-center mt-3">
          <p>
            ¿No tienes cuenta?{' '}
            <button
              className="btn btn-link p-0"
              style={{
                color: '#0d6efd',
                textDecoration: 'underline',
                background: 'none',
                border: 'none',
              }}
              onClick={() => navigate('/register')}
            >
              Crear cuenta
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
