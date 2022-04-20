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
            'answers': [
                'Red', 
                'Orange', 
                'Black',
                'Green'
            ]
        },
        {
            'question': 'What is your favorite number?',
            'answers': [
                '7',
                '13',
                '3',
                '9'
            ]
        },
        {
            'question': 'What is your favorite country?',
            'answers': [
                'USA',
                'Czech Republic',
                'Porto',
                'Budapest'
            ]
        },
        {
            'question': 'What is the best state?',
            'answers': [
                'Florida',
                'Florida',
                'Florida',
                'Florida'
            ]
        }
        ]

    index = 0
    for x in data:
        x['index'] = index
        index += 1

    if setIndex is not None:
        data = [x for x in data if setIndex==x['index']]
    return data


