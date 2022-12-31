from django.forms import ModelForm
from django import forms
from apps.authentication.models import TwitterUser
class ImageForm(forms.ModelForm):
    class Meta:
        model = TwitterUser
        fields = ['image']