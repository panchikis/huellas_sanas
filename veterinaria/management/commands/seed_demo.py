from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from veterinaria.models import Cita, Mascota


PACIENTES = [
    ("Luna", "Perro", "Labrador", "Ana Torres"),
    ("Milo", "Gato", "Siamés", "Carlos Ruiz"),
    ("Nala", "Perro", "Criollo", "María Gómez"),
    ("Simba", "Gato", "Persa", "Jorge Díaz"),
    ("Rocky", "Perro", "Bulldog", "Lucía Pérez"),
    ("Mía", "Gato", "Criollo", "Diego Flores"),
    ("Toby", "Perro", "Beagle", "Sofía Reyes"),
    ("Coco", "Ave", "Canario", "Elena Cruz"),
    ("Kira", "Perro", "Pastor alemán", "Andrés Silva"),
    ("Tom", "Gato", "Mestizo", "Valeria León"),
    ("Bobby", "Perro", "Poodle", "Mateo Castro"),
    ("Pelusa", "Conejo", "Enano", "Paula Ríos"),
    ("Max", "Perro", "Schnauzer", "Daniela Vega"),
    ("Michi", "Gato", "Angora", "Fernando Soto"),
    ("Daisy", "Perro", "Golden retriever", "Camila Ortiz"),
    ("Paco", "Ave", "Periquito", "Ricardo Luna"),
    ("Bella", "Perro", "Chihuahua", "Gabriela Mora"),
    ("Oliver", "Gato", "Bengalí", "Emilio Navarro"),
    ("Chispa", "Perro", "Mestizo", "Natalia Campos"),
    ("Pinky", "Roedor", "Hámster", "Hugo Medina"),
]

MOTIVOS = [
    "Consulta general",
    "Vacunación",
    "Control de rutina",
    "Revisión dental",
    "Desparasitación",
]


class Command(BaseCommand):
    help = "Crea 20 mascotas y citas de demostración de forma repetible."

    def handle(self, *args, **options):
        fecha = timezone.localdate()
        creadas_mascotas = 0
        creadas_citas = 0

        for indice, (nombre, especie, raza, propietario) in enumerate(PACIENTES):
            mascota, creada = Mascota.objects.get_or_create(
                nombre=nombre,
                propietario=propietario,
                defaults={
                    "especie": especie,
                    "raza": raza,
                    "edad": 1 + indice % 14,
                },
            )
            creadas_mascotas += int(creada)
            hora = time(9 + indice // 3, (indice % 3) * 20)
            _, creada = Cita.objects.get_or_create(
                mascota=mascota,
                fecha=fecha,
                hora=hora,
                defaults={
                    "motivo": MOTIVOS[indice % len(MOTIVOS)],
                    "estado": Cita.ESTADOS[indice % len(Cita.ESTADOS)][0],
                },
            )
            creadas_citas += int(creada)

        self.stdout.write(
            self.style.SUCCESS(
                f"Datos listos: {creadas_mascotas} mascotas nuevas y "
                f"{creadas_citas} citas nuevas para {fecha}."
            )
        )
