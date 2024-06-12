from dataclasses import field
from django import forms
from .models import Template, Exercise

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name']


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            'name',
            'sets'
        ]

# ExerciseFormSet = inlineformset_factory(
#     Template, 
#     Exercise, 
#     form=ExerciseForm, 
#     fields=['name', 'sets'], 
#     extra=1
# )