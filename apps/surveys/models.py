from django.db import models

# Create your models here.
class MiscDocs(models.Model):
    EMAIL = models.TextField()
    NAME = models.TextField()