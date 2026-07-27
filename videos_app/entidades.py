"""
Clases de dominio en Programación Orientada a Objetos.

Estas clases (Persona y Video) NO son modelos de Django: son objetos
"puros" de Python que encapsulan los datos y las reglas de negocio del
sistema. Se construyen a partir de los datos capturados en los formularios,
se validan a sí mismas (encapsulamiento mediante propiedades), se pueden
"imprimir" (representación legible para el usuario) y finalmente se
"guardan" delegando la persistencia a los modelos ORM de models.py.

El mismo objeto Persona se reutiliza durante todo el recorrido del usuario
(registro -> confirmación -> captura de cada video -> resumen), viajando
serializado en la sesión HTTP y reconstruyéndose con Persona.capturar().
"""
from .models import PersonaModel, VideoModel
from .validators import (
    validar_alfanumerico,
    validar_alfanumerico_con_espacios,
    validar_solo_letras,
    validar_numero_positivo,
    validar_extension,
    validar_tamano,
)


class Persona:
    """Representa al usuario que se registra para subir videos."""

    def __init__(self, id_nomina=None, nombre=None, cantidad_videos=None):
        # Atributos "privados" (encapsulamiento): se accede a ellos solo
        # a través de las propiedades definidas más abajo, que validan
        # cada valor antes de asignarlo.
        self._id_nomina = None
        self._nombre = None
        self._cantidad_videos = None

        if id_nomina is not None:
            self.id_nomina = id_nomina
        if nombre is not None:
            self.nombre = nombre
        if cantidad_videos is not None:
            self.cantidad_videos = cantidad_videos

    # -- Propiedades con validación (encapsulamiento) --------------------
    @property
    def id_nomina(self):
        return self._id_nomina

    @id_nomina.setter
    def id_nomina(self, valor):
        self._id_nomina = validar_alfanumerico(valor, 'El ID/número de nómina')

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_solo_letras(valor, 'El nombre')

    @property
    def cantidad_videos(self):
        return self._cantidad_videos

    @cantidad_videos.setter
    def cantidad_videos(self, valor):
        self._cantidad_videos = validar_numero_positivo(valor, 'La cantidad de videos')

    # -- Métodos de la clase ---------------------------------------------
    @classmethod
    def capturar(cls, datos):
        """
        Construye un objeto Persona a partir de un diccionario de datos
        (normalmente `form.cleaned_data` o la sesión HTTP).
        """
        try:
            return cls(
                id_nomina=datos.get('id_nomina'),
                nombre=datos.get('nombre'),
                cantidad_videos=datos.get('cantidad_videos'),
            )
        except Exception:
            # Se re-lanza para que la vista decida cómo mostrar el error;
            # 'finally' se usa aquí solo a modo de bitácora del intento.
            raise
        finally:
            pass

    def imprimir(self):
        """Devuelve una representación legible del objeto para el usuario."""
        return (
            f'Bienvenido {self.nombre}, tu número de nómina es {self.id_nomina} '
            f'y estás intentando subir {self.cantidad_videos} videos.'
        )

    def a_diccionario(self):
        """Serializa el objeto para poder guardarlo en la sesión HTTP."""
        return {
            'id_nomina': self.id_nomina,
            'nombre': self.nombre,
            'cantidad_videos': self.cantidad_videos,
        }

    def guardar(self, usuario=None):
        """
        Persiste (crea o actualiza) esta Persona en la base de datos.

        `usuario` es la cuenta de Django (User) con la que esta persona
        inicia sesión; se vincula únicamente al crear la persona por
        primera vez (registro), para poder ver después sus videos pasados.
        """
        registro = None
        try:
            defaults = {
                'nombre': self.nombre,
                'cantidad_videos': self.cantidad_videos,
            }
            if usuario is not None:
                defaults['usuario'] = usuario
            registro, _creado = PersonaModel.objects.update_or_create(
                id_nomina=self.id_nomina,
                defaults=defaults,
            )
        except Exception as error:
            raise RuntimeError(f'No fue posible guardar a la persona: {error}') from error
        finally:
            # Punto único de salida: útil para depuración/telemetría futura.
            pass
        return registro

    def __str__(self):
        return self.imprimir()


class Video:
    """
    Representa un video que la persona desea subir al sistema.

    La extensión y el tamaño ya NO se capturan a mano: se derivan del
    archivo real que el usuario adjunta (self.archivo), validando que la
    extensión pertenezca al catálogo permitido y que el tamaño no supere
    los 3 MB.
    """

    def __init__(self, titulo=None, nombre=None, archivo=None):
        self._titulo = None
        self._nombre = None
        self._archivo = None
        self._extension = None
        self._tamano = None

        if titulo is not None:
            self.titulo = titulo
        if nombre is not None:
            self.nombre = nombre
        if archivo is not None:
            self.archivo = archivo

    # -- Propiedades con validación (encapsulamiento) --------------------
    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._titulo = validar_alfanumerico_con_espacios(valor, 'El título')

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_alfanumerico_con_espacios(valor, 'El nombre del video')

    @property
    def archivo(self):
        return self._archivo

    @archivo.setter
    def archivo(self, valor):
        """
        Recibe el archivo subido (UploadedFile de Django) y deriva de él
        la extensión y el tamaño, validando ambos.
        """
        nombre_archivo = getattr(valor, 'name', '') or ''
        extension_bruta = nombre_archivo.rsplit('.', 1)[-1] if '.' in nombre_archivo else ''
        tamano_bruto = getattr(valor, 'size', 0) / (1024 * 1024)  # bytes -> MB

        self._extension = validar_extension(extension_bruta)
        self._tamano = validar_tamano(tamano_bruto)
        self._archivo = valor

    @property
    def extension(self):
        """Extensión detectada automáticamente a partir del archivo."""
        return self._extension

    @property
    def tamano(self):
        """Tamaño en MB, calculado automáticamente a partir del archivo."""
        return self._tamano

    # -- Métodos de la clase ---------------------------------------------
    @classmethod
    def capturar(cls, datos):
        """Construye un objeto Video a partir de un diccionario de datos."""
        try:
            return cls(
                titulo=datos.get('titulo'),
                nombre=datos.get('nombre'),
                archivo=datos.get('archivo'),
            )
        except Exception:
            raise
        finally:
            pass

    def imprimir(self):
        """Devuelve una representación legible del video."""
        return (
            f'Título: {self.titulo} | Nombre: {self.nombre}.{self.extension} '
            f'| Tamaño: {self.tamano:.2f} MB'
        )

    def guardar(self, persona_registro):
        """
        Persiste este Video en la base de datos, asociado a la
        PersonaModel ya guardada (persona_registro).
        """
        registro = None
        try:
            registro = VideoModel.objects.create(
                persona=persona_registro,
                titulo=self.titulo,
                nombre=self.nombre,
                archivo=self.archivo,
                extension=self.extension,
                tamano_mb=round(self.tamano, 2),
            )
        except Exception as error:
            raise RuntimeError(f'No fue posible guardar el video: {error}') from error
        finally:
            pass
        return registro

    def __str__(self):
        return self.imprimir()
