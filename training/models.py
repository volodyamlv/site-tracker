from django.db import models
from users.models import User

# Create your models here.
class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'template'

class Exercise(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    sets = models.IntegerField()

    class Meta:
        db_table = 'exercise'
