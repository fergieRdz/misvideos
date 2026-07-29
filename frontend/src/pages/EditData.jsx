import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Field from '../components/Field';
import { api } from '../api';

export default function EditData() {
  const [form, setForm] = useState({ nombre: '', cantidad_videos: '' });
  const [persona, setPersona] = useState(null);
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    api.getEdit().then(data => {
      setPersona(data);
      setForm({ nombre: data.nombre, cantidad_videos: String(data.cantidad_videos) });
    });
  }, []);

  function handleChange(e) {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErrors({});
    setMessage(null);
    setLoading(true);
    try {
      await api.putEdit({ ...form, cantidad_videos: Number(form.cantidad_videos) });
      setMessage({ type: 'success', text: 'Tu información fue actualizada.' });
      setTimeout(() => navigate('/confirmar'), 900);
    } catch (err) {
      setErrors(err.errors || {});
      if (err.error) setMessage({ type: 'error', text: err.error });
    } finally {
      setLoading(false);
    }
  }

  const messages = message ? [message] : [];

  return (
    <Layout messages={messages}>
      <section className="tarjeta tarjeta--angosta">
        <div style={{ display: 'flex', alignItems: 'center', gap: '.75rem', marginBottom: '1.5rem' }}>
          <span style={{ fontSize: '2rem' }}>✏️</span>
          <div>
            <h1 className="tarjeta__titulo" style={{ marginBottom: 0 }}>Editar información</h1>
            {persona && (
              <p style={{ color: 'var(--text-soft)', fontSize: '.875rem', marginTop: '.15rem' }}>
                Nómina <strong>{persona.id_nomina}</strong> · no editable
              </p>
            )}
          </div>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <Field label="Nombre completo" id="nombre" name="nombre"
            value={form.nombre} onChange={handleChange} error={errors.nombre}
          />
          <Field label="Cantidad de videos" type="number" id="cantidad_videos" name="cantidad_videos"
            value={form.cantidad_videos} onChange={handleChange} min="1" error={errors.cantidad_videos}
          />
          <div className="acciones">
            <button type="submit" className="boton boton--guardar" disabled={loading}>
              {loading ? 'Guardando...' : '💾 Guardar cambios'}
            </button>
            <button type="button" onClick={() => navigate('/confirmar')} className="boton boton--cancelar">
              Cancelar
            </button>
          </div>
        </form>
      </section>
    </Layout>
  );
}
