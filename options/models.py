from django.db import models

# Create your models here.
class Values(models.Model):
    abc= models.CharField(max_length=250)

    