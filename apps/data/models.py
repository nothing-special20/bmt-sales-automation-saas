from django.db import models

# Create your models here.
class PermitData(models.Model):
    COUNTY = models.TextField()
    DATE = models.DateField(null=True, blank=True)
    RECORD_TYPE = models.TextField(null=True, blank=True)
    RECORD_NUMBER = models.TextField(null=True, blank=True)
    STATUS = models.TextField(null=True, blank=True)
    ACTION = models.TextField(null=True, blank=True)
    ADDRESS = models.TextField(null=True, blank=True)
    PROJECT_NAME = models.TextField(null=True, blank=True)
    EXPIRATION_DATE = models.DateField(null=True, blank=True)
    DESCRIPTION = models.TextField(null=True, blank=True)
    LOAD_DATE_TIME = models.DateTimeField()
    LICENSE_TYPE = models.TextField(null=True, blank=True)

class PermitDataOtherDetails(models.Model):
    RECORD_NUMBER = models.TextField(null=True, blank=True)
    JOB_VALUE = models.TextField(null=True, blank=True)
    CONSTRUCTION_TYPE = models.TextField(null=True, blank=True)
    PERMIT_TYPE = models.TextField(null=True, blank=True)
    SUBPERMIT_TYPE = models.TextField(null=True, blank=True)
    CONSTRUCTION_VALUE = models.TextField(null=True, blank=True)
    WORK_AREA = models.TextField(null=True, blank=True)
    PARCEL_NUMBER = models.TextField(null=True, blank=True)
    AC_UNIT_MAKE = models.TextField(null=True, blank=True)
    AC_UNIT_MODEL = models.TextField(null=True, blank=True)
    ADDITIONAL_COSTS = models.TextField(null=True, blank=True)
    EXISTING_STRUCTURE_ADDITIONS = models.TextField(null=True, blank=True)
    NUM_ROOF_AC_UNITS = models.TextField(null=True, blank=True)
    RES_OR_COMM = models.TextField(null=True, blank=True)
    LOAD_DATE_TIME = models.DateTimeField()

class PermitDataProfessionals(models.Model):
    RECORD_NUMBER = models.TextField(null=True, blank=True)
    PROFESSIONALS = models.TextField(null=True, blank=True)
    LOAD_DATE_TIME = models.DateTimeField()