"""Endpoints REST para el frontend React."""
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.authtoken.models import Token

from .entidades import Persona, Video
from .forms import RegistroForm, EditarPersonaForm, VideoForm
from django.db.models import Q
from .models import PersonaModel, VideoModel
from .validators import EXTENSIONES_VALIDAS, TAMANO_MAXIMO_MB

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    form = RegistroForm(request.data)
    if not form.is_valid():
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        persona = Persona.capturar(form.cleaned_data)
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        persona.guardar(usuario=user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'ok': True})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def confirm(request):
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    persona = Persona(
        id_nomina=persona_registro.id_nomina,
        nombre=persona_registro.nombre,
        cantidad_videos=persona_registro.cantidad_videos,
    )

    if request.method == 'GET':
        return Response({
            'id_nomina': persona_registro.id_nomina,
            'nombre': persona_registro.nombre,
            'cantidad_videos': persona_registro.cantidad_videos,
            'videos_capturados': persona_registro.videos_capturados,
            'mensaje': persona.imprimir(),
        })

    respuesta = request.data.get('respuesta')
    if respuesta == 'si':
        return Response({'redirect': f'/video/{persona_registro.videos_capturados + 1}'})
    if respuesta == 'no':
        return Response({'redirect': '/opciones'})
    return Response({'error': 'Respuesta inválida.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit(request):
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)

    if request.method == 'GET':
        return Response({
            'id_nomina': persona_registro.id_nomina,
            'nombre': persona_registro.nombre,
            'cantidad_videos': persona_registro.cantidad_videos,
        })

    form = EditarPersonaForm(request.data)
    if not form.is_valid():
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        persona = Persona(
            id_nomina=persona_registro.id_nomina,
            nombre=form.cleaned_data['nombre'],
            cantidad_videos=form.cleaned_data['cantidad_videos'],
        )
        persona.guardar()
        return Response({'ok': True})
    except RuntimeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, JSONParser])
def video(request, numero):
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    total = persona_registro.cantidad_videos
    siguiente_natural = persona_registro.videos_capturados + 1

    if numero > total:
        return Response({'redirect': '/historial'})
    if numero != siguiente_natural:
        return Response({'redirect': f'/video/{siguiente_natural}'})

    if request.method == 'GET':
        return Response({
            'numero': numero,
            'total': total,
            'persona': {
                'nombre': persona_registro.nombre,
                'id_nomina': persona_registro.id_nomina,
            },
            'extensiones_validas': list(EXTENSIONES_VALIDAS),
            'tamano_maximo_mb': TAMANO_MAXIMO_MB,
        })

    if request.data.get('accion') == 'cancelar':
        return Response({'redirect': '/historial'})

    form = VideoForm(request.data, request.FILES)
    if not form.is_valid():
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        video_obj = Video.capturar(form.cleaned_data)
        video_obj.guardar(persona_registro)
        siguiente = numero + 1
        if siguiente <= total:
            return Response({'redirect': f'/video/{siguiente}'})
        return Response({'redirect': '/historial'})
    except RuntimeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_video(request, video_id):
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    video = get_object_or_404(VideoModel, id=video_id, persona=persona_registro)
    if video.archivo:
        video.archivo.delete(save=False)
    video.delete()
    return Response({'ok': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    persona_registro = get_object_or_404(PersonaModel, usuario=request.user)
    q = request.query_params.get('q', '').strip()
    videos = persona_registro.videos.all()
    if q:
        videos = videos.filter(Q(titulo__icontains=q) | Q(nombre__icontains=q))
    return Response({
        'persona': {
            'nombre': persona_registro.nombre,
            'id_nomina': persona_registro.id_nomina,
            'cantidad_videos': persona_registro.cantidad_videos,
            'videos_capturados': persona_registro.videos_capturados,
        },
        'videos': [
            {
                'id': v.id,
                'titulo': v.titulo,
                'nombre': v.nombre,
                'extension': v.extension,
                'tamano_mb': str(v.tamano_mb),
                'archivo_url': v.archivo.url if v.archivo else None,
            }
            for v in videos
        ],
    })
