import os

import django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .functions import mock_data, twilio_sms

# Create your views here.

def send_message(request):
    print(request.POST)
    index = int(request.POST.get('index'))
    print(index)
    data = mock_data('', index)[0]
    first_name = data['firstName']
    phone = data['phone']
    msg = first_name + ' ' + request.POST.get('msg')
    twilio_sms(phone, msg)
    return follow_up(request)

def follow_up(request):
    cold_leads = mock_data('Cold Leads')
    requested_quotes = mock_data('Requested Quotes')
    scheduled_calls = mock_data('Scheduled Calls')
    scheduled_appointments = mock_data('Scheduled Appointments')
    closed_deals = mock_data('Closed Deals')
    return render(request, 'follow_up/landing_page.html', 
        {
            'cold_leads_count': len(cold_leads),
            'cold_leads': cold_leads,
            'requested_quotes_count': len(requested_quotes),
            'requested_quotes': requested_quotes,
            'scheduled_calls_count': len(scheduled_calls),
            'scheduled_calls': scheduled_calls,
            'scheduled_appointments_count': len(scheduled_appointments),
            'scheduled_appointments': scheduled_appointments,
            'closed_deals_count': len(closed_deals),
            'closed_deals': closed_deals
        }
    )

