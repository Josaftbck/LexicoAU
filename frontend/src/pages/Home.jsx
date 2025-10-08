import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <h1 className="home-title">Bienvenido al Sistema SportGo</h1>
      <p className="home-subtitle">
        Explora los módulos del panel desde el menú lateral. Gestiona usuarios, inventario y configuraciones con un entorno moderno y dinámico.
      </p>

      <div className="home-cards">
        <div className="home-card">
          <h3>Usuarios</h3>
          <p>Gestiona perfiles y accesos del sistema.</p>
        </div>
        <div className="home-card alt">
          <h3>Inventario</h3>
          <p>Controla productos, existencias y movimientos.</p>
        </div>
        <div className="home-card">
          <h3>Reportes</h3>
          <p>Visualiza estadísticas y métricas clave.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
