// components/LogoutButton.jsx
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt } from 'react-icons/fa';

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
    <button onClick={handleLogout} className="btn btn-danger d-flex align-items-center">
      <FaSignOutAlt className="me-2" />
      Cerrar sesión
    </button>
  );
}

export default LogoutButton;
