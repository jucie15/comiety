from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User   # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from dongzip.models import Profile

class UserForm(UserCreationForm):
    username = forms.EmailField(required = True, help_text='주로 사용하는 이메일 주소를 입력해 주세요.', max_length =150)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['school','nickname','tel_number','profile_image',]
