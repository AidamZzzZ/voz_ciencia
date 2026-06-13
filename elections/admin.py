from django.contrib import admin
from .models import Campana, Plancha, Votante, AuditoriaVoto

@admin.register(Campana)
class CampanaAdmin(admin.ModelAdmin):
    list_display = ('nombre_campana', 'fecha_inicio', 'fecha_cierre', 'esta_activa')
    list_filter = ('esta_activa',)
    search_fields = ('nombre_campana',)

@admin.register(Plancha)
class PlanchaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'candidato_principal', 'campana', 'votos_recibidos')
    list_filter = ('campana',)
    search_fields = ('nombre', 'candidato_principal')

@admin.register(Votante)
class VotanteAdmin(admin.ModelAdmin):
    list_display = ('token_sesion', 'campana', 'ya_voto', 'fecha_voto')
    list_filter = ('campana', 'ya_voto')
    search_fields = ('token_sesion',)

@admin.register(AuditoriaVoto)
class AuditoriaVotoAdmin(admin.ModelAdmin):
    list_display = ('comprobante', 'fecha_emision', 'campana')
    list_filter = ('campana',)
    search_fields = ('comprobante',)
