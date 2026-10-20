from django import forms

from .models import Cita, Mascota


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ["nombre", "especie", "raza", "edad", "propietario"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej. Luna"}),
            "especie": forms.TextInput(attrs={"placeholder": "Ej. Perro"}),
            "raza": forms.TextInput(attrs={"placeholder": "Ej. Labrador"}),
            "edad": forms.NumberInput(attrs={"min": 0, "placeholder": "Opcional"}),
            "propietario": forms.TextInput(attrs={"placeholder": "Nombre completo"}),
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["mascota", "fecha", "hora", "motivo", "estado"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "motivo": forms.Textarea(attrs={"rows": 3}),
        }
