from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date

from .forms import CitaForm, MascotaForm
from .models import Cita


def agenda(request):
    fecha_seleccionada = request.GET.get("fecha")
    if fecha_seleccionada is None:
        fecha = timezone.localdate()
    elif fecha_seleccionada.strip():
        fecha = parse_date(fecha_seleccionada)
    else:
        fecha = None

    if fecha_seleccionada and fecha is None:
        return HttpResponseBadRequest("La fecha debe tener el formato AAAA-MM-DD.")

    estado = request.GET.get("estado", "")
    estados_validos = {valor for valor, _ in Cita.ESTADOS}
    if estado and estado not in estados_validos:
        return HttpResponseBadRequest("El estado de la cita no es válido.")

    titulos_todas_las_fechas = {
        "": "Citas de todos los estados en todas las fechas",
        "pendiente": "Citas pendientes de todas las fechas",
        "atendida": "Citas atendidas de todas las fechas",
        "cancelada": "Citas canceladas de todas las fechas",
    }

    citas = Cita.objects.all().select_related("mascota")
    if fecha is not None:
        citas = citas.filter(fecha=fecha)
    if estado:
        citas = citas.filter(estado=estado)

    return render(
        request,
        "veterinaria/agenda.html",
        {
            "citas": citas,
            "fecha": fecha,
            "todas_las_fechas": fecha is None,
            "estado_seleccionado": estado,
            "titulo_todas_las_fechas": titulos_todas_las_fechas[estado],
            "estados": Cita.ESTADOS,
        },
    )


def nueva_mascota(request):
    form = MascotaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        mascota = form.save()
        messages.success(request, f"{mascota.nombre} se registró correctamente.")
        return redirect("veterinaria:agenda")

    return render(request, "veterinaria/mascota_form.html", {"form": form})


def nueva_cita(request):
    form = CitaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cita = form.save()
        messages.success(request, f"La cita de {cita.mascota} se guardó correctamente.")
        return redirect("veterinaria:agenda")

    return render(
        request,
        "veterinaria/cita_form.html",
        {
            "form": form,
            "hay_mascotas": form.fields["mascota"].queryset.exists(),
        },
    )


def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    form = CitaForm(request.POST or None, instance=cita)
    if request.method == "POST" and form.is_valid():
        cita = form.save()
        messages.success(request, f"La cita de {cita.mascota} se actualizó correctamente.")
        return redirect("veterinaria:agenda")

    return render(
        request,
        "veterinaria/cita_form.html",
        {
            "form": form,
            "hay_mascotas": form.fields["mascota"].queryset.exists(),
            "es_edicion": True,
        },
    )
