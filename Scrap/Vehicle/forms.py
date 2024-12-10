from django import forms
from .models import Car , Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"