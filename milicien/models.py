from django.db import models

# Create your models here.
class Namelist(models.Model):
    name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    invitorID = models.IntegerField()
    phone = models.CharField(max_length=12)
    active = models.BooleanField()
