from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

from .admin import CitaAdmin
from .models import Cita, Mascota


class AgendaTests(TestCase):
    def setUp(self):
        self.mascota = Mascota.objects.create(
            nombre="Luna",
            especie="Perro",
            raza="Labrador",
            propietario="Ana Torres",
        )

    def test_agenda_muestra_citas_del_dia_seleccionado(self):
        cita = Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-20",
            hora="09:00",
            motivo="Consulta general",
        )

        response = self.client.get(
            reverse("veterinaria:agenda"),
            {"fecha": "2026-10-20"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, cita.mascota.nombre)
        self.assertContains(response, "Consulta general")

    def test_agenda_rechaza_fecha_invalida(self):
        response = self.client.get(
            reverse("veterinaria:agenda"),
            {"fecha": "fecha-invalida"},
        )

        self.assertEqual(response.status_code, 400)

    def test_fecha_vacia_muestra_todos_los_estados_de_todas_las_fechas(self):
        pendiente_pasada = Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-19",
            hora="09:00",
            motivo="Control pendiente",
        )
        Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-21",
            hora="10:00",
            motivo="Cita atendida",
            estado="atendida",
        )
        cancelada = Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-22",
            hora="11:00",
            motivo="Cita cancelada",
            estado="cancelada",
        )

        response = self.client.get(
            reverse("veterinaria:agenda"),
            {"fecha": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Citas de todos los estados en todas las fechas")
        self.assertContains(response, "Control pendiente")
        self.assertContains(response, "Cita atendida")
        self.assertContains(response, "Cita cancelada")
        self.assertContains(response, "19/10/2026")
        self.assertContains(response, "21/10/2026")
        self.assertContains(response, "22/10/2026")
        self.assertEqual(
            set(response.context["citas"]),
            {pendiente_pasada, *Cita.objects.exclude(pk=pendiente_pasada.pk)},
        )

    def test_fecha_vacia_filtra_por_estado_seleccionado(self):
        Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-19",
            hora="09:00",
            motivo="Control pendiente",
            estado="pendiente",
        )
        atendida = Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-21",
            hora="10:00",
            motivo="Cita atendida",
            estado="atendida",
        )

        response = self.client.get(
            reverse("veterinaria:agenda"),
            {"fecha": "", "estado": "atendida"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Citas atendidas de todas las fechas")
        self.assertContains(response, "Cita atendida")
        self.assertNotContains(response, "Control pendiente")
        self.assertEqual(list(response.context["citas"]), [atendida])

    def test_cita_se_puede_editar_incluyendo_fecha_y_estado(self):
        cita = Cita.objects.create(
            mascota=self.mascota,
            fecha="2026-10-20",
            hora="09:00",
            motivo="Consulta general",
        )
        url = reverse("veterinaria:editar_cita", args=[cita.pk])

        response = self.client.post(
            url,
            {
                "mascota": self.mascota.pk,
                "fecha": "2026-10-25",
                "hora": "12:30",
                "motivo": "Control actualizado",
                "estado": "atendida",
            },
        )

        self.assertRedirects(response, reverse("veterinaria:agenda"))
        cita.refresh_from_db()
        self.assertEqual(cita.fecha.isoformat(), "2026-10-25")
        self.assertEqual(cita.hora.strftime("%H:%M"), "12:30")
        self.assertEqual(cita.motivo, "Control actualizado")
        self.assertEqual(cita.estado, "atendida")

    def test_recepcionista_puede_registrar_mascota(self):
        response = self.client.post(
            reverse("veterinaria:nueva_mascota"),
            {
                "nombre": "Nala",
                "especie": "Perro",
                "raza": "Criollo",
                "edad": "",
                "propietario": "María Gómez",
            },
        )

        self.assertRedirects(response, reverse("veterinaria:agenda"))
        self.assertTrue(Mascota.objects.filter(nombre="Nala").exists())

    def test_recepcionista_puede_agendar_cita(self):
        response = self.client.post(
            reverse("veterinaria:nueva_cita"),
            {
                "mascota": self.mascota.pk,
                "fecha": "2026-10-20",
                "hora": "10:30",
                "motivo": "Vacunación",
                "estado": "pendiente",
            },
        )

        self.assertRedirects(response, reverse("veterinaria:agenda"))
        self.assertTrue(
            Cita.objects.filter(mascota=self.mascota, motivo="Vacunación").exists()
        )

    def test_admin_filtra_citas_por_fecha_y_estado(self):
        self.assertIn("fecha", CitaAdmin.list_filter)
        self.assertIn("estado", CitaAdmin.list_filter)


class DatosDemostracionTests(TestCase):
    def test_comando_crea_20_mascotas_y_citas_y_es_repetible(self):
        call_command("seed_demo", verbosity=0)
        self.assertEqual(Mascota.objects.count(), 20)
        self.assertEqual(Cita.objects.count(), 20)

        call_command("seed_demo", verbosity=0)
        self.assertEqual(Mascota.objects.count(), 20)
        self.assertEqual(Cita.objects.count(), 20)
