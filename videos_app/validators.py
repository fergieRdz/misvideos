"""
Reglas de validación reutilizadas por los formularios de Django y por las
clases de dominio (Persona, Video). Centralizar las reglas aquí evita
duplicar expresiones regulares o límites numéricos en varios lugares.
"""
import re

from django.core.exceptions import ValidationError

# Extensiones de video aceptadas por el sistema.
EXTENSIONES_VALIDAS = ('mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm')

# Tamaño máximo permitido por video, en megabytes.
TAMANO_MAXIMO_MB = 3.0

_PATRON_ALFANUMERICO = re.compile(r'^[A-Za-z0-9]+$')
_PATRON_ALFANUMERICO_ESPACIOS = re.compile(r'^[A-Za-z0-9 ]+$')
_PATRON_SOLO_LETRAS = re.compile(r'^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$')


def validar_alfanumerico(valor, nombre_campo='El campo'):
    """Verifica que el valor contenga únicamente letras y números."""
    if not valor or not _PATRON_ALFANUMERICO.match(str(valor).strip()):
        raise ValidationError(
            f'{nombre_campo} debe ser alfanumérico (solo letras y números, sin espacios ni símbolos).'
        )
    return str(valor).strip()


def validar_alfanumerico_con_espacios(valor, nombre_campo='El campo'):
    """Verifica que el valor contenga letras, números y espacios."""
    if not valor or not _PATRON_ALFANUMERICO_ESPACIOS.match(str(valor).strip()):
        raise ValidationError(
            f'{nombre_campo} debe ser alfanumérico (letras y números, sin símbolos).'
        )
    return str(valor).strip()


def validar_solo_letras(valor, nombre_campo='El campo'):
    """Verifica que el valor contenga únicamente letras (y espacios)."""
    if not valor or not _PATRON_SOLO_LETRAS.match(str(valor).strip()):
        raise ValidationError(f'{nombre_campo} debe contener únicamente letras.')
    return str(valor).strip()


def validar_numero_positivo(valor, nombre_campo='El campo'):
    """Verifica que el valor sea un entero positivo."""
    try:
        numero = int(str(valor).strip())
    except (TypeError, ValueError):
        raise ValidationError(f'{nombre_campo} debe ser un valor numérico entero.')
    if numero <= 0:
        raise ValidationError(f'{nombre_campo} debe ser mayor a cero.')
    return numero


def validar_extension(valor):
    """Verifica que la extensión pertenezca al catálogo de extensiones válidas."""
    extension = str(valor).strip().lower().lstrip('.')
    if extension not in EXTENSIONES_VALIDAS:
        raise ValidationError(
            'Extensión no válida. Usa una de: ' + ', '.join(EXTENSIONES_VALIDAS) + '.'
        )
    return extension


def validar_tamano(valor):
    """Verifica que el tamaño sea numérico, positivo y no exceda el máximo permitido."""
    try:
        tamano = float(str(valor).strip())
    except (TypeError, ValueError):
        raise ValidationError('El tamaño debe ser un valor numérico.')
    if tamano <= 0:
        raise ValidationError('El tamaño debe ser mayor a cero.')
    if tamano > TAMANO_MAXIMO_MB:
        raise ValidationError(f'El tamaño no debe superar los {TAMANO_MAXIMO_MB:.0f} MB.')
    return tamano
