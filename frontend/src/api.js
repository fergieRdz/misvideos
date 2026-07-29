const BASE = import.meta.env.VITE_API_URL || '';

function getToken() {
  return localStorage.getItem('token');
}

async function request(method, path, body = null, isFormData = false) {
  const headers = {};
  const token = getToken();
  if (token) headers['Authorization'] = `Token ${token}`;
  if (!isFormData) headers['Content-Type'] = 'application/json';

  const opts = { method, headers };
  if (body) opts.body = isFormData ? body : JSON.stringify(body);

  const res = await fetch(`${BASE}${path}`, opts);
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export const api = {
  register:    (data)         => request('POST', '/api/auth/register/', data),
  login:       (data)         => request('POST', '/api/auth/login/', data),
  logout:      ()             => request('POST', '/api/auth/logout/'),
  getConfirm:  ()             => request('GET',  '/api/confirm/'),
  postConfirm: (respuesta)    => request('POST', '/api/confirm/', { respuesta }),
  getEdit:     ()             => request('GET',  '/api/edit/'),
  putEdit:     (data)         => request('PUT',  '/api/edit/', data),
  getVideo:    (numero)       => request('GET',  `/api/video/${numero}/`),
  postVideo:   (numero, fd)   => request('POST', `/api/video/${numero}/`, fd, true),
  getHistory:  (q = '')       => request('GET',  `/api/history/${q ? `?q=${encodeURIComponent(q)}` : ''}`),
  deleteVideo: (id)           => request('DELETE', `/api/video/${id}/delete/`),
};
