import re
import json
import sys
import os

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import TemporaryUploadedFile

from .models import EmailCollector

"""
    Function that loads files from a folder into elasticsearch
    Source: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
"""

def email_collector(email, name):
    record = EmailCollector(EMAIL=email, NAME=name)
    record.save()
    print('it works!')
    print([email, name])