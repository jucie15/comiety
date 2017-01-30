from django.forms import ModelForm
from .models import Society

class SocietyForm(ModelForm):
    class Meta:
        model = Society
        fields = '__all__'
