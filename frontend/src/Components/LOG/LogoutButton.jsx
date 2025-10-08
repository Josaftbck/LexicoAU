import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt } from 'react-icons/fa';
import './LogoutButton.css'; // ✅ nuevo archivo de estilos

function LogoutButton() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    if (window.confirm('¿Estás seguro que deseas cerrar sesión?')) {
      logout();
      navigate('/login', { replace: true });
    }
  };

  return (
    <button className="logout-btn" onClick={handleLogout}>
      <FaSignOutAlt className="logout-icon" />
      <span className="logout-text">Cerrar sesión</span>
    </button>
  );
}

export default LogoutButton;

