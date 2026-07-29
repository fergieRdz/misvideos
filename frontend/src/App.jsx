import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Confirm from './pages/Confirm';
import OptionsNo from './pages/OptionsNo';
import EditData from './pages/EditData';
import VideoUpload from './pages/VideoUpload';
import History from './pages/History';

function PrivateRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" replace />;
}

function PublicRoute({ children }) {
  const { token } = useAuth();
  return !token ? children : <Navigate to="/historial" replace />;
}

function Routes_() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/historial" replace />} />
      <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/registro" element={<PublicRoute><Register /></PublicRoute>} />
      <Route path="/confirmar" element={<PrivateRoute><Confirm /></PrivateRoute>} />
      <Route path="/opciones" element={<PrivateRoute><OptionsNo /></PrivateRoute>} />
      <Route path="/editar" element={<PrivateRoute><EditData /></PrivateRoute>} />
      <Route path="/video/:numero" element={<PrivateRoute><VideoUpload /></PrivateRoute>} />
      <Route path="/historial" element={<PrivateRoute><History /></PrivateRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes_ />
    </AuthProvider>
  );
}
