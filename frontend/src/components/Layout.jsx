import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { api } from '../api';

export default function Layout({ children, messages = [] }) {
  const { token, username, clearAuth } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    try { await api.logout(); } catch (_) {}
    clearAuth();
    navigate('/login');
  }

  return (
    <>
      <header className="encabezado">
        <div className="contenedor encabezado__interior">
          <Link to="/" className="marca">
            🎬 Mis Videos
          </Link>
          <nav className="encabezado__nav">
            {token ? (
              <>
                <span className="encabezado__usuario">👤 {username}</span>
                <Link to="/historial" className="enlace-nav">Mis videos</Link>
                <button onClick={handleLogout} className="enlace-nav enlace-nav--boton">
                  Cerrar sesión
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="enlace-nav">Iniciar sesión</Link>
                <Link to="/registro" className="enlace-nav">Crear cuenta</Link>
              </>
            )}
          </nav>
        </div>
      </header>

      <div className="hero-bar">
        <p>Registro y administración de tus videos</p>
      </div>

      <main className="contenedor contenido">
        {messages.length > 0 && (
          <ul className="mensajes">
            {messages.map((m, i) => (
              <li key={i} className={`mensaje mensaje--${m.type}`}>{m.text}</li>
            ))}
          </ul>
        )}
        {children}
      </main>

      <footer className="pie">
        <div className="contenedor">
          <p>Mis Videos &mdash; Trabajo final · Python · Django · PostgreSQL · React</p>
        </div>
      </footer>
    </>
  );
}
