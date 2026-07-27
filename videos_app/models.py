"""
Modelos ORM de Django. Definen las tablas reales en la base de datos
PostgreSQL "Pro_Gol":

- PersonaModel: usuarios registrados (número de nómina, nombre, cantidad
  de videos que desean subir).
- VideoModel: videos capturados, relacionados con PersonaModel mediante
  una llave foránea (relación uno a muchos).

Estas clases son la capa de persistencia. La lógica de negocio y las
validaciones "de dominio" viven en videos_app.entidades (clases Persona y
Video en Programación Orientada a Objetos), que son las que la aplicación
usa y reutiliza a lo largo de todo el flujo antes de guardar en estas tablas.
"""
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import EXTENSIONES_VALIDAS, TAMANO_MAXIMO_MB


class PersonaModel(models.Model):
    """Tabla de usuarios registrados en el sistema."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='persona',
        null=True,
        blank=True,
        help_text='Cuenta (usuario/contraseña) con la que esta persona inicia sesión.',
    )
    id_nomina = models.CharField(
        'ID / número de nómina',
        max_length=20,
        unique=True,
        help_text='Identificador alfanumérico único del usuario.',
    )
    nombre = models.CharField('Nombre completo', max_length=150)
    cantidad_videos = models.PositiveIntegerField(
        'Cantidad de videos a subir',
        validators=[MinValueValidator(1)],
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'personas'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombre} ({self.id_nomina})'

    @property
    def videos_capturados(self):
        """Cantidad de videos que ya se guardaron para esta persona."""
        return self.videos.count()

    @property
    def registro_completo(self):
        """True si ya se capturaron todos los videos prometidos."""
        return self.videos_capturados >= self.cantidad_videos


class VideoModel(models.Model):
    """Tabla de videos, relacionada con PersonaModel."""

    persona = models.ForeignKey(
        PersonaModel,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name='Persona',
    )
    titulo = models.CharField('Título', max_length=150)
    nombre = models.CharField('Nombre del video', max_length=150)
    archivo = models.FileField('Archivo de video', upload_to='videos/%Y/%m/%d/')
    extension = models.CharField(
        'Extensión',
        max_length=10,
        choices=[(ext, ext.upper()) for ext in EXTENSIONES_VALIDAS],
        help_text='Se detecta automáticamente a partir del archivo subido.',
    )
    tamano_mb = models.DecimalField(
        'Tamaño (MB)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(TAMANO_MAXIMO_MB)],
        help_text='Se calcula automáticamente a partir del archivo subido.',
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['id']

    def __str__(self):
        return f'{self.nombre}.{self.extension} ({self.tamano_mb} MB)'
