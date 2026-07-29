"""Rutas de la aplicación 'videos_app'."""
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'videos_app'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(
        template_name='videos_app/login.html',
        redirect_authenticated_user=True,
    ), name='iniciar_sesion'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='videos_app:iniciar_sesion',
    ), name='cerrar_sesion'),
    path('confirmar/', views.confirmar_datos, name='confirmar_datos'),
    path('confirmar/no/', views.opciones_no, name='opciones_no'),
    path('editar/', views.editar_datos, name='editar_datos'),
    path('video/<int:numero>/', views.registro_video, name='registro_video'),
    path('historial/', views.historial, name='historial'),
    path('video/<int:video_id>/eliminar/', views.eliminar_video, name='eliminar_video'),
]
