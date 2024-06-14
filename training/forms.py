from django import forms
from .models import Template


class TemplateForm(forms.ModelForm):
    name = forms.CharField(label='Название шаблона', max_length=50, required=True)
    class Meta:
        model = Template
        fields = ["name"]