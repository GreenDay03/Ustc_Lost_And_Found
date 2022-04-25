from django.db import models

# Create your models here.
class Qa(models.Model):
    id = models.AutoField(primary_key=True)
    q = models.CharField(max_length=100)
    a = models.CharField(max_length=1000)
    time = models.DateTimeField()
    top = models.BooleanField()

