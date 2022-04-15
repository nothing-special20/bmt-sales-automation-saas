import re
import json
import sys
import os

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import TemporaryUploadedFile

"""
    Function that loads files from a folder into elasticsearch
    Source: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
"""

def mock_data(setIndex=None):
    data = [
        {
            'question': 'What is your favorite color?',
            'answer_1': 'Red',
            'answer_2': 'Orange',
            'answer_3': 'Black',
            'answer_4': 'Green'
        },
        {
            'question': 'What is your favorite number?',
            'answer_1': '7',
            'answer_2': '13',
            'answer_3': '3',
            'answer_4': '9'
        },
        {
            'question': 'What is your favorite country?',
            'answer_1': 'USA',
            'answer_2': 'Czech Republic',
            'answer_3': 'Porto',
            'answer_4': 'Budapest'
        }
        ]

    index = 0
    for x in data:
        x['index'] = index
        index += 1

    if setIndex is not None:
        data = [x for x in data if setIndex==x['index']]
    return data


