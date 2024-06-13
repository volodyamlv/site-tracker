from django import forms
from .models import WorkoutHistory

class WorkoutHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkoutHistory
        exclude = ['template_name', 'exercise_name', 'user', 'date_created']    