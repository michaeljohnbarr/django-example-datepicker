from django.db import models

# Create your models here.
class TestModel(models.Model):
    start = models.DateField()
    end = models.DateField()
