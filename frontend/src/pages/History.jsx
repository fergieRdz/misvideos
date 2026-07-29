import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { api } from '../api';

const BROWSER_PLAYABLE = ['mp4', 'webm', 'mov'];
const BASE = import.meta.env.VITE_API_URL || '';

export default function History() {
  const [data, setData] = useState(null);
  const [query, setQuery] = useState('');
  const [search, setSearch] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const load = useCallback((q = '') => {
    setError('');
    api.getHistory(q)
      .then(setData)
      .catch(() => setError('No se pudo cargar el historial.'));
  }, []);

  useEffect(() => { load(); }, [load]);

  function handleSearch(e) {
    e.preventDefault();
    setSearch(query);
    load(query);
  }

  function handleClear() {
    setQuery('');
    setSearch('');
    load('');
  }

  async function handleDelete(video) {
    if (!window.confirm(`¿Eliminar «${video.titulo}»? Esta acción no se puede deshacer.`)) return;
    try {
      await api.deleteVideo(video.id);
      load(search);
    } catch {
      setError('No se pudo eliminar el video.');
    }
  }

  const messages = error ? [{ type: 'error', text: error }] : [];

  if (!data) return <Layout messages={messages}><p style={{ color: 'var(--text-soft)', padding: '2rem 0' }}>Cargando...</p></Layout>;

  const { persona, videos } = data;
  const pct = Math.round((persona.videos_capturados / persona.cantidad_videos) * 100) || 0;

  return (
    <Layout messages={messages}>
      <section className="tarjeta">
        <h1 className="tarjeta__titulo">Mis videos</h1>

        <div className="stats-chip">
          🎞 {persona.videos_capturados} de {persona.cantidad_videos} videos guardados
        </div>

        <p className="tarjeta__descripcion">
          <strong>{persona.nombre}</strong> &nbsp;·&nbsp; nómina <strong>{persona.id_nomina}</strong>
        </p>

        <div className="progreso" style={{ marginBottom: '1.75rem' }}>
          <div className="progreso__barra" style={{ width: `${pct}%` }} />
        </div>

        <form onSubmit={handleSearch} className="buscador">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Buscar por título o nombre…"
          />
          <button type="submit" className="boton boton--primario" style={{ padding: '.7rem 1.25rem' }}>
            🔍 Buscar
          </button>
          {search && (
            <button type="button" onClick={handleClear} className="boton boton--cancelar" style={{ padding: '.7rem 1rem' }}>
              Limpiar
            </button>
          )}
        </form>

        <div className="tabla-scroll">
          <table className="tabla">
            <thead>
              <tr>
                <th>#</th><th>Título</th><th>Nombre</th>
                <th>Ext.</th><th>MB</th><th>Video</th><th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {videos.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-soft)' }}>
                    {search ? `No se encontraron videos con «${search}».` : 'Aún no se ha guardado ningún video.'}
                  </td>
                </tr>
              ) : videos.map((v, i) => (
                <tr key={v.id}>
                  <td style={{ color: 'var(--text-soft)', fontWeight: 600 }}>{i + 1}</td>
                  <td style={{ fontWeight: 600 }}>{v.titulo}</td>
                  <td>{v.nombre}</td>
                  <td>
                    <span style={{ background: '#eef2ff', color: 'var(--primary-dark)', borderRadius: 6, padding: '.2rem .55rem', fontSize: '.78rem', fontWeight: 700 }}>
                      {v.extension.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-soft)' }}>{v.tamano_mb}</td>
                  <td>
                    {v.archivo_url
                      ? BROWSER_PLAYABLE.includes(v.extension)
                        ? (
                          <video controls>
                            <source src={`${BASE}${v.archivo_url}`} type={`video/${v.extension}`} />
                          </video>
                        )
                        : <a href={`${BASE}${v.archivo_url}`} target="_blank" rel="noopener noreferrer">⬇ Descargar</a>
                      : <span style={{ color: 'var(--text-xsoft)' }}>Sin archivo</span>
                    }
                  </td>
                  <td>
                    <button
                      onClick={() => handleDelete(v)}
                      className="boton boton--cancelar"
                      style={{ padding: '.38rem .8rem', fontSize: '.82rem' }}
                    >
                      🗑 Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {persona.videos_capturados < persona.cantidad_videos && (
          <div className="acciones" style={{ marginTop: '1.5rem' }}>
            <button
              onClick={() => navigate(`/video/${persona.videos_capturados + 1}`)}
              className="boton boton--guardar"
            >
              ➕ Continuar subiendo videos ({persona.videos_capturados} / {persona.cantidad_videos})
            </button>
          </div>
        )}
      </section>
    </Layout>
  );
}
