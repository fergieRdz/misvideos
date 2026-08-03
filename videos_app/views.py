"""
Vistas de 'Mis Videos'.

Ahora el sistema requiere una cuenta (usuario/contraseña) para poder subir
y, sobre todo, para volver a iniciar sesión y consultar los videos
capturados en el pasado. El recorrido es:

    1) registro         -> crea la cuenta y captura ID/nómina, nombre y
                            cantidad de videos a subir (queda con la
                            sesión iniciada).
    2) confirmar_datos   -> muestra el mensaje de confirmación (Sí/No).
    3) opciones_no       -> si respondió "No": corregir información o
                             salir del sistema (cerrar sesión).
    4) editar_datos      -> corrige nombre/cantidad de videos.
    5) registro_video    -> captura Título/Nombre/Archivo, uno por uno,
                             tantas veces como videos indicó.
    6) historial         -> "mis videos": lo guardado en la base de datos
                             para la cuenta con la que se inició sesión.

Todas las pantallas posteriores al registro requieren sesión iniciada
(@login_required), y cada persona solo puede ver/editar su propia
información (siempre se busca por request.user, nunca por un id que
viaje en la URL o en la sesión).
"""
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .entidades import Persona, Video
from .forms import RegistroForm, EditarPersonaForm, VideoForm
from .models import PersonaModel, VideoModel

CLAVE_SESION_PERSONA = 'persona'


def inicio(request):
    """Raíz del sitio: cada quien a su pantalla según si ya inició sesión."""
    if request.user.is_authenticated:
        return redirect('videos_app:historial')
    return redirect('videos_app:registro')


def registro(request):
    """Paso 1: crea la cuenta (usuario/contraseña) y los datos de la persona."""
    if request.user.is_authenticated:
        return redirect('videos_app:historial')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                persona = Persona.capturar(form.cleaned_data)
                with transaction.atomic():
                    nuevo_usuario = get_user_model().objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                    )
                    persona.guardar(usuario=nuevo_usuario)
            except Exception as error:
                messages.error(request, f'No se pudo completar el registro: {error}')
            else:
                login(request, nuevo_usuario, backend='django.contrib.auth.backends.ModelBackend')
                request.session[CLAVE_SESION_PERSONA] = persona.a_diccionario()
                return redirect('videos_app:confirmar_datos')
            finally:
                pass
    else:
        form = RegistroForm()

    return render(request, 'videos_app/registro.html', {'form': form})


@login_required
def confirmar_datos(request):
    """Paso 2: muestra el mensaje de confirmación y procesa Sí/No."""
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    persona = Persona(
        id_nomina=persona_registro.id_nomina,
        nombre=persona_registro.nombre,
        cantidad_videos=persona_registro.cantidad_videos,
    )

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')

        if respuesta == 'si':
            return redirect('videos_app:registro_video', numero=persona_registro.videos_capturados + 1)

        if respuesta == 'no':
            return redirect('videos_app:opciones_no')

    return render(request, 'videos_app/confirmacion.html', {
        'persona': persona,
        'mensaje': persona.imprimir(),
    })


@login_required
def opciones_no(request):
    """Paso 3: el usuario respondió 'No' -> corregir información o salir."""
    return render(request, 'videos_app/opciones_no.html')


@login_required
def editar_datos(request):
    """Corrige nombre y/o cantidad de videos (el ID/nómina no cambia)."""
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)

    if request.method == 'POST':
        form = EditarPersonaForm(request.POST)
        if form.is_valid():
            try:
                persona = Persona(
                    id_nomina=persona_registro.id_nomina,
                    nombre=form.cleaned_data['nombre'],
                    cantidad_videos=form.cleaned_data['cantidad_videos'],
                )
                persona.guardar()
            except RuntimeError as error:
                messages.error(request, str(error))
            else:
                messages.success(request, 'Tu información fue actualizada.')
                return redirect('videos_app:confirmar_datos')
    else:
        form = EditarPersonaForm(initial={
            'nombre': persona_registro.nombre,
            'cantidad_videos': persona_registro.cantidad_videos,
        })

    return render(request, 'videos_app/editar_datos.html', {
        'form': form,
        'persona': persona_registro,
    })


@login_required
def registro_video(request, numero):
    """Paso 5: captura los datos de un video específico (1..cantidad_videos)."""
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    total = persona_registro.cantidad_videos
    siguiente_natural = persona_registro.videos_capturados + 1

    if numero > total:
        return redirect('videos_app:historial')
    if numero != siguiente_natural:
        # Evita huecos o repeticiones: siempre se captura el próximo video pendiente.
        return redirect('videos_app:registro_video', numero=siguiente_natural)

    if request.method == 'POST':
        if request.POST.get('accion') == 'cancelar':
            messages.info(request, 'Se canceló la captura de este video.')
            return redirect('videos_app:historial')

        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                video = Video.capturar(form.cleaned_data)
                video.guardar(persona_registro)
            except RuntimeError as error:
                messages.error(request, str(error))
            else:
                siguiente = numero + 1
                if siguiente <= total:
                    return redirect('videos_app:registro_video', numero=siguiente)
                return redirect('videos_app:historial')
            finally:
                pass
    else:
        form = VideoForm()

    return render(request, 'videos_app/registro_video.html', {
        'form': form,
        'numero': numero,
        'total': total,
        'persona': persona_registro,
    })


@login_required
def historial(request):
    """'Mis videos': muestra la persona y todos sus videos guardados."""
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    q = request.GET.get('q', '').strip()
    videos_bd = persona_registro.videos.all()
    if q:
        videos_bd = videos_bd.filter(Q(titulo__icontains=q) | Q(nombre__icontains=q))

    return render(request, 'videos_app/historial.html', {
        'persona': persona_registro,
        'videos': videos_bd,
        'q': q,
    })


@login_required
def eliminar_video(request, video_id):
    """Elimina un video (registro + archivo físico) que pertenezca al usuario."""
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    video = get_object_or_404(VideoModel, id=video_id, persona=persona_registro)
    if request.method == 'POST':
        if video.archivo:
            video.archivo.delete(save=False)
        video.delete()
        messages.success(request, 'Video eliminado correctamente.')
    return redirect('videos_app:historial')
