import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { api } from '../api';

export default function Confirm() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    api.getConfirm()
      .then(setData)
      .catch(() => setError('No se pudieron cargar los datos.'))
      .finally(() => setLoading(false));
  }, []);

  async function handleAnswer(respuesta) {
    try {
      const result = await api.postConfirm(respuesta);
      navigate(result.redirect);
    } catch {
      setError('Error al procesar la respuesta.');
    }
  }

  const messages = error ? [{ type: 'error', text: error }] : [];

  if (loading) return <Layout><p style={{ color: 'var(--text-soft)', padding: '2rem 0' }}>Cargando...</p></Layout>;

  return (
    <Layout messages={messages}>
      <section className="tarjeta tarjeta--angosta tarjeta--centrada">
        <div style={{ fontSize: '2.5rem', marginBottom: '.75rem' }}>✅</div>
        <h1 className="tarjeta__titulo">Confirma tu información</h1>
        {data && <p className="mensaje-confirmacion">{data.mensaje}</p>}
        <p style={{ color: 'var(--text-soft)', marginBottom: '1.5rem' }}>
          ¿La información es correcta?
        </p>
        <div className="acciones acciones--centradas">
          <button onClick={() => handleAnswer('si')} className="boton boton--guardar" style={{ minWidth: 120 }}>
            ✓ Sí, continuar
          </button>
          <button onClick={() => handleAnswer('no')} className="boton boton--cancelar" style={{ minWidth: 120 }}>
            ✗ No, corregir
          </button>
        </div>
      </section>
    </Layout>
  );
}
