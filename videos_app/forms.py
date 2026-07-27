"""
Formularios de Django. Se encargan de la presentación HTML y de invocar
las mismas funciones de validación usadas por las clases de dominio
(videos_app.validators), evitando así duplicar las reglas de negocio.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import PersonaModel
from .validators import (
    EXTENSIONES_VALIDAS,
    TAMANO_MAXIMO_MB,
    validar_alfanumerico,
    validar_alfanumerico_con_espacios,
    validar_solo_letras,
    validar_extension,
    validar_tamano,
)


class RegistroForm(forms.Form):
    """
    Formulario de registro: crea la cuenta (usuario/contraseña) con la que
    la persona podrá volver a iniciar sesión para ver sus videos pasados,
    junto con sus datos (ID/nómina, nombre, cantidad de videos a subir).
    """

    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. jperez', 'autocomplete': 'username'}),
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    id_nomina = forms.CharField(
        label='ID / número de nómina',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej. A12345',
            'autocomplete': 'off',
        }),
    )
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej. Juana Pérez López',
            'autocomplete': 'off',
        }),
    )
    cantidad_videos = forms.IntegerField(
        label='Cantidad de videos que deseas subir',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Ej. 3'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Ese nombre de usuario ya está en uso.')
        return username

    def clean_id_nomina(self):
        id_nomina = validar_alfanumerico(self.cleaned_data['id_nomina'], 'El ID/número de nómina')
        if PersonaModel.objects.filter(id_nomina=id_nomina).exists():
            raise forms.ValidationError('Ese número de nómina ya está registrado con otra cuenta.')
        return id_nomina

    def clean_nombre(self):
        return validar_solo_letras(self.cleaned_data['nombre'], 'El nombre')

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        if password1:
            try:
                validate_password(password1)
            except DjangoValidationError as error:
                self.add_error('password1', error)
        return cleaned


class EditarPersonaForm(forms.Form):
    """Permite corregir nombre y cantidad de videos (el ID/nómina no cambia)."""

    nombre = forms.CharField(
        label='Nombre completo',
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    cantidad_videos = forms.IntegerField(
        label='Cantidad de videos que deseas subir',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Ej. 3'}),
    )

    def clean_nombre(self):
        return validar_solo_letras(self.cleaned_data['nombre'], 'El nombre')


class VideoForm(forms.Form):
    """Captura los datos de cada video que la persona quiere subir."""

    titulo = forms.CharField(
        label='Título',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Resumen del proyecto'}),
    )
    nombre = forms.CharField(
        label='Nombre del video',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. proyecto final 2026'}),
    )
    archivo = forms.FileField(
        label='Archivo de video',
        help_text=(
            f'Formatos permitidos: {", ".join(EXTENSIONES_VALIDAS)}. '
            f'Tamaño máximo {TAMANO_MAXIMO_MB:.0f} MB.'
        ),
        widget=forms.ClearableFileInput(attrs={
            'accept': ','.join(f'.{ext}' for ext in EXTENSIONES_VALIDAS),
        }),
    )

    def clean_titulo(self):
        return validar_alfanumerico_con_espacios(self.cleaned_data['titulo'], 'El título')

    def clean_nombre(self):
        return validar_alfanumerico_con_espacios(self.cleaned_data['nombre'], 'El nombre del video')

    def clean_archivo(self):
        """
        La extensión y el tamaño ya no se capturan a mano: se derivan del
        archivo real que el usuario adjunta, reutilizando las mismas
        reglas de validación que usa la clase de dominio Video.
        """
        archivo = self.cleaned_data['archivo']
        extension_bruta = archivo.name.rsplit('.', 1)[-1] if '.' in archivo.name else ''
        validar_extension(extension_bruta)
        validar_tamano(archivo.size / (1024 * 1024))
        return archivo
