import os

import django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .functions import mock_data

# Create your views here.

survey_data = {'survey_data': mock_data()}


def follow_up(request):
    if request.user.is_authenticated:
        return render(request, 'surveys/surveys.html', survey_data)

    else:
        return render(request, 'web/landing_page.html')

