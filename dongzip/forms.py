from django.forms import ModelForm
from .models import Society, Profile

class SocietyForm(ModelForm):
    class Meta:
        model = Society
        #fields = '__all__'
        fields = ['school', 'name', 'main_tel_number', 'address', 'description', 'users']