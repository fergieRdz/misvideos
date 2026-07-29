import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import Field from '../components/Field';
import { api } from '../api';

export default function VideoUpload() {
  const { numero } = useParams();
  const [info, setInfo] = useState(null);
  const [form, setForm] = useState({ titulo: '', nombre: '' });
  const [archivo, setArchivo] = useState(null);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setForm({ titulo: '', nombre: '' });
    setArchivo(null);
    setErrors({});
    api.getVideo(numero).then(data => {
      if (data.redirect) { navigate(data.redirect); return; }
      setInfo(data);
    });
  }, [numero]);

  function handleChange(e) {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErrors({});
    setLoading(true);
    const fd = new FormData();
    fd.append('titulo', form.titulo);
    fd.append('nombre', form.nombre);
    if (archivo) fd.append('archivo', archivo);
    try {
      const result = await api.postVideo(numero, fd);
      navigate(result.redirect);
    } catch (err) {
      const errs = err.errors || {};
      if (err.error) errs.__all__ = [err.error];
      setErrors(errs);
    } finally {
      setLoading(false);
    }
  }

  async function handleCancel() {
    const fd = new FormData();
    fd.append('accion', 'cancelar');
    try {
      const result = await api.postVideo(numero, fd);
      navigate(result.redirect);
    } catch {
      navigate('/historial');
    }
  }

  if (!info) return <Layout><p style={{ color: 'var(--text-soft)', padding: '2rem 0' }}>Cargando...</p></Layout>;

  const pct = Math.round((Number(numero) / info.total) * 100);
  const globalError = errors.__all__?.[0];
  const messages = globalError ? [{ type: 'error', text: globalError }] : [];

  return (
    <Layout messages={messages}>
      <section className="tarjeta tarjeta--angosta">
        <div style={{ display: 'flex', alignItems: 'center', gap: '.75rem', marginBottom: '.5rem' }}>
          <span style={{ fontSize: '2rem' }}>🎥</span>
          <div>
            <h1 className="tarjeta__titulo" style={{ marginBottom: 0 }}>
              Video {numero} de {info.total}
            </h1>
            <p style={{ color: 'var(--text-soft)', fontSize: '.875rem', marginTop: '.15rem' }}>
              {info.persona.nombre} · nómina {info.persona.id_nomina}
            </p>
          </div>
        </div>

        <div className="progreso">
          <div className="progreso__barra" style={{ width: `${pct}%` }} />
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <Field label="Título" id="titulo" name="titulo"
            value={form.titulo} onChange={handleChange}
            placeholder="Ej. Resumen del proyecto" error={errors.titulo}
          />
          <Field label="Nombre del video" id="nombre" name="nombre"
            value={form.nombre} onChange={handleChange}
            placeholder="Ej. proyecto final 2026" error={errors.nombre}
          />

          <div className="campo">
            <label htmlFor="archivo">Archivo de video</label>
            <input
              id="archivo"
              type="file"
              accept={info.extensiones_validas.map(e => `.${e}`).join(',')}
              onChange={e => setArchivo(e.target.files[0] || null)}
            />
            <p className="campo__ayuda">
              Formatos: {info.extensiones_validas.join(', ')} · Máximo {info.tamano_maximo_mb} MB
            </p>
            {errors.archivo && (
              <ul className="campo__errores">
                {(Array.isArray(errors.archivo) ? errors.archivo : [errors.archivo]).map((e, i) => (
                  <li key={i}>{e}</li>
                ))}
              </ul>
            )}
          </div>

          <div className="acciones">
            <button type="submit" className="boton boton--guardar" disabled={loading}>
              {loading ? 'Guardando...' : '💾 Guardar video'}
            </button>
            <button type="button" onClick={handleCancel} className="boton boton--cancelar">
              Cancelar
            </button>
          </div>
        </form>
      </section>
    </Layout>
  );
}
