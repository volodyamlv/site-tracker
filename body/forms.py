from django import forms
from .models import Body

class BodyForm(forms.ModelForm):
    class Meta:
        model = Body
        fields = ['forearm', 'arm', 'chest', 'waist', 'hips', 'pelvis', 'weight']
