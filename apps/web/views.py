from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .functions import email_collector

def home(request):
    if request.user.is_authenticated:
        return render(request, 'web/app_home.html', context={
            'active_tab': 'dashboard',
        })
    else:
        if request.method == 'POST':
            email = request.POST.get('prospectEmail')
            name = request.POST.get('prospectName')
            email_collector(email, name)
            return render(request, 'web/landing_page.html')
        else:
            return render(request, 'web/landing_page.html')