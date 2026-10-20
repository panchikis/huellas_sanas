from django.db import models


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    propietario = models.CharField(max_length=100, verbose_name="Nombre del dueño")

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("atendida", "Atendida"),
        ("cancelada", "Cancelada"),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name="citas")
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    class Meta:
        ordering = ["fecha", "hora"]

    def __str__(self):
        return f"Cita de {self.mascota} el {self.fecha} a las {self.hora}"