import { useState } from 'react';

export default function Field({ label, type = 'text', id, error, help, ...props }) {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === 'password';
  const inputType = isPassword ? (showPassword ? 'text' : 'password') : type;

  return (
    <div className="campo">
      <label htmlFor={id}>{label}</label>
      {isPassword ? (
        <div className="campo__password">
          <input id={id} type={inputType} {...props} />
          <button
            type="button"
            className="campo__ojo"
            onClick={() => setShowPassword(v => !v)}
            aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
          >
            {showPassword ? '🙈' : '👁'}
          </button>
        </div>
      ) : (
        <input id={id} type={inputType} {...props} />
      )}
      {help && <p className="campo__ayuda">{help}</p>}
      {error && (
        <ul className="campo__errores">
          {(Array.isArray(error) ? error : [error]).map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
