import { useState } from "react";
import { NavLink } from "react-router-dom";
import { FaBars, FaHome, FaUserAlt, FaCog, FaSignOutAlt, FaChartPie, FaBox } from "react-icons/fa";
import LogoutButton from "./LOG/LogoutButton";
import "./Sidebar.css";

function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`sidebar-container ${isOpen ? "open" : "collapsed"}`}>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-icon">🌀</span>
          <span className={`logo-text ${!isOpen && "hidden"}`}>SportGo</span>
        </div>
        <button className="toggle-btn" onClick={toggleSidebar}>
          <FaBars />
        </button>
      </div>

      <ul className="sidebar-nav">
        <li>
          <NavLink to="/dashboard" className="nav-item">
            <FaHome className="nav-icon" />
            <span className={`nav-text ${!isOpen && "hidden"}`}>Dashboard</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/users" className="nav-item">
            <FaUserAlt className="nav-icon" />
            <span className={`nav-text ${!isOpen && "hidden"}`}>Users</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/analytics" className="nav-item">
            <FaChartPie className="nav-icon" />
            <span className={`nav-text ${!isOpen && "hidden"}`}>Analytics</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/inventory" className="nav-item">
            <FaBox className="nav-icon" />
            <span className={`nav-text ${!isOpen && "hidden"}`}>Inventory</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/settings" className="nav-item">
            <FaCog className="nav-icon" />
            <span className={`nav-text ${!isOpen && "hidden"}`}>Settings</span>
          </NavLink>
        </li>
      </ul>

      <div className="sidebar-footer">
        <LogoutButton />
        <FaSignOutAlt className="nav-icon logout-icon" />
      </div>
    </div>
  );
}

export default Sidebar;
