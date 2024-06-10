from django import forms
from .models import mitarbeiter

class MitarbeiterForm(forms.ModelForm):
    class Meta:
        model = mitarbeiter
        fields = ['vorname', 'name']
