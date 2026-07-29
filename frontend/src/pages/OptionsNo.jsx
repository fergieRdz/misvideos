import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { useAuth } from '../AuthContext';
import { api } from '../api';

export default function OptionsNo() {
  const navigate = useNavigate();
  const { clearAuth } = useAuth();

  async function handleLogout() {
    try { await api.logout(); } catch (_) {}
    clearAuth();
    navigate('/login');
  }

  return (
    <Layout>
      <section className="tarjeta tarjeta--angosta tarjeta--centrada">
        <div style={{ fontSize: '2.5rem', marginBottom: '.75rem' }}>🤔</div>
        <h1 className="tarjeta__titulo">¿Qué deseas hacer?</h1>
        <p className="tarjeta__descripcion">
          Puedes corregir tu información o salir del sistema.
        </p>
        <div className="acciones acciones--centradas">
          <button onClick={() => navigate('/editar')} className="boton boton--guardar" style={{ minWidth: 180 }}>
            ✏️ Corregir información
          </button>
          <button onClick={handleLogout} className="boton boton--cancelar" style={{ minWidth: 180 }}>
            🚪 Salir del sistema
          </button>
        </div>
      </section>
    </Layout>
  );
}
