from django.db import models

# Create your models here.
class EmailCollector(models.Model):
    EMAIL = models.TextField()
    NAME = models.TextField()