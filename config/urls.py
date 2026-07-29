"""Rutas raíz del proyecto 'Mis Videos'."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from videos_app import api_views

api_patterns = [
    path('auth/register/', api_views.register),
    path('auth/login/', api_views.login_view),
    path('auth/logout/', api_views.logout_view),
    path('confirm/', api_views.confirm),
    path('edit/', api_views.edit),
    path('video/<int:numero>/', api_views.video),
    path('video/<int:video_id>/delete/', api_views.delete_video),
    path('history/', api_views.history),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('', include('videos_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
