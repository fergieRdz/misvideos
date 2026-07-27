from django.contrib import admin

from .models import PersonaModel, VideoModel


class VideoInline(admin.TabularInline):
    model = VideoModel
    extra = 0


@admin.register(PersonaModel)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id_nomina', 'nombre', 'usuario', 'cantidad_videos', 'videos_capturados', 'fecha_registro')
    search_fields = ('id_nomina', 'nombre', 'usuario__username')
    inlines = [VideoInline]


@admin.register(VideoModel)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'extension', 'tamano_mb', 'persona', 'fecha_subida')
    list_filter = ('extension',)
    search_fields = ('nombre', 'titulo')
