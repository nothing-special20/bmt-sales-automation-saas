import os

import django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .functions import mock_data, twilio_sms

# Create your views here.

cold_leads = mock_data('Cold Leads')
requested_quotes = mock_data('Requested Quotes')
scheduled_calls = mock_data('Scheduled Calls')
scheduled_appointments = mock_data('Scheduled Appointments')
closed_deals = mock_data('Closed Deals')

misc_values = {
        'cold_leads_count': len(cold_leads),
        'cold_leads': cold_leads,
        'requested_quotes_count': len(requested_quotes),
        'requested_quotes': requested_quotes,
        'scheduled_calls_count': len(scheduled_calls),
        'scheduled_calls': scheduled_calls,
        'scheduled_appointments_count': len(scheduled_appointments),
        'scheduled_appointments': scheduled_appointments,
        'closed_deals_count': len(closed_deals),
        'closed_deals': closed_deals,
        'msgBody': '',
        'msgSubject': ''   
    }

def send_message(request):
    print(request.POST)
    index = request.POST.get('index').split('~')
    category = index[0]
    index_num = int(index[1])
    print(index)
    data = mock_data(category, index_num)[0]
    first_name = data['firstName']
    phone = data['phone']
    msg = first_name + ' ' + misc_values['msgBody']
    twilio_sms(phone, msg)
    return follow_up(request)

def set_message(request):
    misc_values['msgBody'] = request.POST.get('msgBody')
    misc_values['msgSubject'] = request.POST.get('msgSubject')
    return follow_up(request)

def follow_up(request):
    return render(request, 'follow_up/landing_page.html', misc_values)

