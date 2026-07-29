import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Layout from '../components/Layout';
import Field from '../components/Field';
import { api } from '../api';
import { useAuth } from '../AuthContext';

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { saveAuth } = useAuth();
  const navigate = useNavigate();

  function handleChange(e) {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await api.login(form);
      saveAuth(data.token, data.username);
      navigate('/historial');
    } catch (err) {
      setError(err.error || 'Error al iniciar sesión.');
    } finally {
      setLoading(false);
    }
  }

  const messages = error ? [{ type: 'error', text: error }] : [];

  return (
    <Layout messages={messages}>
      <section className="tarjeta tarjeta--angosta">
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '.5rem' }}>🎬</div>
          <h1 className="tarjeta__titulo">Bienvenido de vuelta</h1>
          <p className="tarjeta__descripcion" style={{ marginBottom: 0 }}>
            Inicia sesión para ver tus videos
          </p>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <Field
            label="Usuario" id="username" name="username"
            value={form.username} onChange={handleChange}
            autoComplete="username" placeholder="Tu nombre de usuario"
          />
          <Field
            label="Contraseña" type="password" id="password" name="password"
            value={form.password} onChange={handleChange}
            autoComplete="current-password" placeholder="Tu contraseña"
          />
          <button type="submit" className="boton boton--guardar" disabled={loading}
            style={{ width: '100%', marginTop: '.5rem', padding: '.85rem' }}>
            {loading ? 'Entrando...' : '→ Entrar'}
          </button>
        </form>

        <div className="divisor">o</div>

        <Link to="/registro" className="boton boton--cancelar" style={{ width: '100%', justifyContent: 'center' }}>
          Crear cuenta nueva
        </Link>
      </section>
    </Layout>
  );
}
