import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Layout from '../components/Layout';
import Field from '../components/Field';
import { api } from '../api';
import { useAuth } from '../AuthContext';

export default function Register() {
  const [form, setForm] = useState({
    username: '', password1: '', password2: '',
    id_nomina: '', nombre: '', cantidad_videos: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const { saveAuth } = useAuth();
  const navigate = useNavigate();

  function handleChange(e) {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErrors({});
    setLoading(true);
    try {
      const payload = { ...form, cantidad_videos: Number(form.cantidad_videos) };
      const data = await api.register(payload);
      saveAuth(data.token, data.username);
      navigate('/confirmar');
    } catch (err) {
      setErrors(err.errors || { __all__: [err.error || 'Error al registrarse.'] });
    } finally {
      setLoading(false);
    }
  }

  const globalError = errors.__all__?.[0];
  const messages = globalError ? [{ type: 'error', text: globalError }] : [];

  return (
    <Layout messages={messages}>
      <section className="tarjeta tarjeta--angosta">
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '.5rem' }}>📝</div>
          <h1 className="tarjeta__titulo">Crear cuenta</h1>
          <p className="tarjeta__descripcion" style={{ marginBottom: 0 }}>
            Regístrate para subir y administrar tus videos
          </p>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <p style={{ fontWeight: 700, fontSize: '.8rem', color: 'var(--text-soft)', textTransform: 'uppercase', letterSpacing: '.06em', marginBottom: '.75rem' }}>
            Acceso
          </p>
          <Field label="Usuario" id="username" name="username"
            value={form.username} onChange={handleChange}
            autoComplete="username" placeholder="Ej. jperez"
            error={errors.username}
          />
          <Field label="Contraseña" type="password" id="password1" name="password1"
            value={form.password1} onChange={handleChange}
            autoComplete="new-password" placeholder="Mínimo 8 caracteres"
            error={errors.password1}
          />
          <Field label="Confirmar contraseña" type="password" id="password2" name="password2"
            value={form.password2} onChange={handleChange}
            autoComplete="new-password" placeholder="Repite la contraseña"
            error={errors.password2}
          />

          <div style={{ borderTop: '1px solid var(--border)', margin: '1.25rem 0', paddingTop: '1.25rem' }}>
            <p style={{ fontWeight: 700, fontSize: '.8rem', color: 'var(--text-soft)', textTransform: 'uppercase', letterSpacing: '.06em', marginBottom: '.75rem' }}>
              Datos personales
            </p>
            <Field label="ID / número de nómina" id="id_nomina" name="id_nomina"
              value={form.id_nomina} onChange={handleChange}
              placeholder="Ej. A12345" error={errors.id_nomina}
            />
            <Field label="Nombre completo" id="nombre" name="nombre"
              value={form.nombre} onChange={handleChange}
              placeholder="Ej. Juana Pérez López" error={errors.nombre}
            />
            <Field label="Cantidad de videos que deseas subir" type="number"
              id="cantidad_videos" name="cantidad_videos"
              value={form.cantidad_videos} onChange={handleChange}
              placeholder="Ej. 3" min="1" error={errors.cantidad_videos}
            />
          </div>

          <button type="submit" className="boton boton--guardar" disabled={loading}
            style={{ width: '100%', padding: '.85rem' }}>
            {loading ? 'Registrando...' : '✓ Crear cuenta'}
          </button>
        </form>

        <div className="divisor">ya tienes cuenta</div>

        <Link to="/login" className="boton boton--cancelar" style={{ width: '100%', justifyContent: 'center' }}>
          Iniciar sesión
        </Link>
      </section>
    </Layout>
  );
}
