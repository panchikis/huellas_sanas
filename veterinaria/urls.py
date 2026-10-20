from django.urls import path

from . import views

app_name = "veterinaria"

urlpatterns = [
    path("", views.agenda, name="agenda"),
    path("mascotas/nueva/", views.nueva_mascota, name="nueva_mascota"),
    path("citas/nueva/", views.nueva_cita, name="nueva_cita"),
    path("citas/<int:cita_id>/editar/", views.editar_cita, name="editar_cita"),
]
