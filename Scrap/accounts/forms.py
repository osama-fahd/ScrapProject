from django import forms
from .models import ProfileSeller

# Create the form class.
class ProfileSellerForm(forms.ModelForm):
    class Meta:
        model = ProfileSeller
        fields = ['specialized', 'company_name', 'google_map_address', 'address', 'commercial_register']