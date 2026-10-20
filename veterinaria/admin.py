from django.contrib import admin

from .models import Cita, Mascota


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especie", "raza", "propietario", "edad")
    search_fields = ("nombre", "propietario", "raza")
    list_filter = ("especie",)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora", "mascota", "motivo", "estado")
    list_filter = ("fecha", "estado")
    date_hierarchy = "fecha"
    search_fields = ("mascota__nombre", "mascota__propietario", "motivo")
    list_select_related = ("mascota",)
