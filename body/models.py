from django.db import models
from users.models import User

class Body(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forearm = models.DecimalField(max_digits=5, decimal_places=2)
    arm = models.DecimalField(max_digits=5, decimal_places=2)
    chest = models.DecimalField(max_digits=5, decimal_places=2)
    waist = models.DecimalField(max_digits=5, decimal_places=2)
    hips = models.DecimalField(max_digits=5, decimal_places=2)
    pelvis = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'body'
