import { Routes, Route } from 'react-router-dom';
import AppNavbar from './Navbar';
import Home from '../pages/Home';



function DashboardApp() {
  return (
    <>
      <AppNavbar /> {/* Navbar solo dentro del dashboard */}
      <div className="container mt-4">
        <Routes>
<Route index element={<Home />} />  {/* Ruta principal del dashboard */}


        </Routes>
      </div>
    </>
  );
}

export default DashboardApp;
