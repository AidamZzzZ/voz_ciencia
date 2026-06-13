from django import forms
from django.forms import inlineformset_factory
from .models import Campana, Plancha

class CampanaForm(forms.ModelForm):
    class Meta:
        model = Campana
        fields = ['nombre_campana', 'fecha_inicio', 'fecha_cierre', 'esta_activa']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_cierre': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PlanchaForm(forms.ModelForm):
    class Meta:
        model = Plancha
        fields = ['nombre', 'candidato_principal', 'propuesta', 'logo']

PlanchaFormSet = inlineformset_factory(
    Campana, Plancha, form=PlanchaForm,
    extra=1, can_delete=True
)
