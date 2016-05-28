from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from customerservice.models import Customer
from customerservice.models import Device

from customerservice.forms import search_forms


def customer_service_index(request, username):
    user_id =  request.session.get('user_id', None)
    if user_id == username:
        template = 'customerservice/customerservice_index.html'
        context = dict()
        context['username'] = username
        context['name_form'] = search_forms.SearchByNameForm()
        context['phone_form'] = search_forms.SearchByPhoneForm()
        return render(request, template, context)
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_search_by_name(request):
    return HttpResponse("Searched by name")


def customer_service_search_by_phone(request):
    user_id = request.session.get('user_id', None)
    if user_id:
        if request.POST:
            form = search_forms.SearchByPhoneForm(request.POST)
            if form.is_valid():
                form_cleaned_data = form.cleaned_data
                try:
                    customer = Customer.objects.get(land_phone_number__exact = form_cleaned_data['phone'])
                    devices = Device.objects.filter(customer__land_phone_number = form_cleaned_data['phone'])
                    template = 'customerservice/customerservice_customers.html'
                    context = dict()
                    context['customer_device'] = [(customer, devices)]
                    return render(request, template, context)
                except Customer.DoesNotExist:
                    return HttpResponse("Not found customer")
            else:
                return HttpResponse("Invalid form data")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)
