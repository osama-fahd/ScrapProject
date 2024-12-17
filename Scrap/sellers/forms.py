from django import forms
from autoparts.models import Product
from accounts.models import Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']