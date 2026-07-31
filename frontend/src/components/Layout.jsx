import { Link, useNavigate, useLocation } from 'react-router-dom';
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

  async function handleAgregarVideo() {
    try {
      const data = await api.getConfirm();
      if (data.videos_capturados < data.cantidad_videos) {
        navigate(`/video/${data.videos_capturados + 1}`);
      } else {
        // quota full — expand it by 1 then go to the new slot
        await api.putEdit({ nombre: data.nombre, cantidad_videos: data.cantidad_videos + 1 });
        navigate(`/video/${data.cantidad_videos + 1}`);
      }
    } catch {
      navigate('/video/1');
    }
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
                <button onClick={handleAgregarVideo} className="enlace-nav enlace-nav--boton">Agregar videos</button>
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
