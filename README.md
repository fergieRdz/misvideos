# Mis Videos

Aplicación web para registrar usuarios y administrar los videos que desean
subir. Construida con **Python, Django, PostgreSQL, HTML y CSS**.

## Arquitectura del proyecto

```
trabajo final/
├── manage.py
├── requirements.txt
├── .env.example              # plantilla de variables de entorno
├── config/                   # configuración del proyecto Django
│   ├── settings.py           # incluye la conexión a PostgreSQL (BD "Pro_Gol")
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── videos_app/                # aplicación principal
    ├── entidades.py            # clases POO: Persona y Video (encapsulamiento)
    ├── validators.py           # reglas de validación reutilizables
    ├── models.py                # modelos ORM: PersonaModel, VideoModel
    ├── forms.py                  # PersonaForm, VideoForm
    ├── views.py                   # flujo del asistente (registro -> confirmación -> videos -> resumen)
    ├── urls.py
    ├── admin.py
    ├── migrations/
    ├── templates/videos_app/       # HTML (base, registro, confirmación, video, resumen...)
    └── static/videos_app/css/      # style.css
```

### Capas y clases POO

- **`videos_app/entidades.py`** contiene las clases de dominio pedidas:
  `Persona` (id, nombre, cantidad_videos) y `Video` (título, nombre,
  extensión, tamaño). Encapsulan sus atributos mediante propiedades que
  validan cada valor, y exponen `capturar()` (construir desde datos de
  formulario), `imprimir()` (representación para el usuario) y
  `guardar()` (persistencia, con manejo de excepciones try/except/finally).
- **`videos_app/models.py`** contiene los modelos ORM de Django
  (`PersonaModel`, `VideoModel`) que definen las tablas reales en
  PostgreSQL y la relación uno-a-muchos entre persona y sus videos.

## Flujo de la aplicación

1. **Registro** (`/`): captura ID/nómina, nombre completo y cantidad de
   videos a subir.
2. **Confirmación** (`/confirmar/`): muestra
   *"Bienvenido [Nombre], tu número de nómina es [ID] y estás intentando
   subir [Cantidad] videos. ¿La información es correcta?"* con botones
   Sí/No.
   - **Sí** → guarda a la persona y pasa a capturar cada video.
   - **No** → permite corregir la información o salir del sistema.
3. **Captura de videos** (`/video/<n>/`): repite el formulario (Título,
   Nombre, Extensión, Tamaño) tantas veces como videos se indicaron,
   validando que el tamaño nunca supere los 3 MB.
4. **Resumen** (`/resumen/`): muestra la persona y todos sus videos
   guardados en PostgreSQL.

## Validaciones implementadas

| Campo                  | Regla                                             |
|------------------------|----------------------------------------------------|
| ID / número de nómina  | Alfanumérico                                       |
| Nombre                 | Solo letras (y espacios)                           |
| Cantidad de videos     | Numérico entero positivo                           |
| Título del video       | Alfanumérico                                       |
| Nombre del video       | Alfanumérico                                       |
| Extensión              | Debe pertenecer al catálogo válido (mp4, avi, mov, mkv, wmv, flv, webm) |
| Tamaño                 | Numérico, mayor a 0 y **máximo 3 MB**              |

Todas las reglas están centralizadas en `videos_app/validators.py` y son
usadas tanto por los formularios de Django (mensajes de error en la
interfaz) como por las clases `Persona`/`Video` (validación de dominio).

## Requisitos previos

- Python 3.10+
- PostgreSQL 14+ en ejecución

## Instalación y ejecución

```bash
# 1) Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL si es necesario

# 4) Crear la base de datos PostgreSQL "Pro_Gol"
psql -U postgres -c 'CREATE DATABASE "Pro_Gol";'

# 5) Aplicar migraciones
python manage.py migrate

# 6) (Opcional) crear un superusuario para /admin/
python manage.py createsuperuser

# 7) Levantar el servidor de desarrollo
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en tu navegador para usar la aplicación.

## Nota sobre este entorno

Para verificar el proyecto de punta a punta se instaló PostgreSQL 16 vía
Homebrew (`brew install postgresql@16`, servicio iniciado con
`brew services start postgresql@16`), se creó la base `Pro_Gol` y el rol
`postgres`/`postgres`, y se ejecutó el flujo completo (registro,
confirmación, captura de videos con validaciones, resumen) contra la base
de datos real. Los datos de prueba usados durante la verificación fueron
eliminados (`TRUNCATE`) al finalizar, dejando las tablas vacías y listas
para uso real.
