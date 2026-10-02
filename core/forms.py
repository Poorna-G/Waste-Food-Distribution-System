from django import forms
from .models import FoodPost

class FoodPostForm(forms.ModelForm):
    class Meta:
        model = FoodPost
        fields = ['food_name', 'quantity', 'location', 'expiry_time', 'description']