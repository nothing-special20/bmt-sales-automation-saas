from django.db import models

# Create your models here.
class MiscDocs(models.Model):
    FILENAME = models.TextField()
    PG_NUM = models.IntegerField()
    DOC_TEXT = models.TextField()