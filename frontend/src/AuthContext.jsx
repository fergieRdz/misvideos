import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [username, setUsername] = useState(() => localStorage.getItem('username'));

  function saveAuth(tok, user) {
    setToken(tok);
    setUsername(user);
    localStorage.setItem('token', tok);
    localStorage.setItem('username', user);
  }

  function clearAuth() {
    setToken(null);
    setUsername(null);
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  }

  return (
    <AuthContext.Provider value={{ token, username, saveAuth, clearAuth }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
