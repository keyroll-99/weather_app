from django import forms
from .models import Weather
class WatherForm(forms.ModelForm):
    class Meta:
        model = Weather
        fields = ['city']