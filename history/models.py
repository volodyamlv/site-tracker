from django.db import models
from users.models import User


# Create your models here.
class WorkoutHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=50)
    exercise_name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.PositiveSmallIntegerField()
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'history'    