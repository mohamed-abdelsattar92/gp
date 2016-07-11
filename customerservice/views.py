from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.urlresolvers import reverse


from customerservice.models import Customer
from customerservice.models import Device
from ticket.models import Ticket
from customerservice.forms import search_forms, device_form, customer_form, ticket_form


def customer_service_index(request, username):
    customerservice_user_id =  request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id == username and customer_service:
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
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        if request.POST:
            form = search_forms.SearchByNameForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                customers = Customer.objects.filter(first_name__contains = f_c_d['first_name'],\
                                                    middle_name__contains = f_c_d['middle_name'],\
                                                    last_name__contains = form.cleaned_data['last_name'])
                if customers:
                    customer_devices = list()
                    for customer in customers:
                        devices = Device.objects.filter(customer__pk = customer.pk)
                        customer_devices.append((customer,devices)) # list of tuples to hold each customer and his devices
                    template = 'customerservice/customerservice_customers.html'
                    context = dict()
                    context['customer_devices'] = customer_devices
                    return render(request, template, context)
                else:
                    return HttpResponse("Not found customer")
            else:
                return HttpResponse("Invalid form data")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_search_by_phone(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        if request.POST:
            form = search_forms.SearchByPhoneForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                customers = Customer.objects.filter(land_phone_number__exact = f_c_d['phone'])
                if customers:
                    customer_devices = list()   # a list to add devices to each customer returned from the query set
                    for customer in customers:
                        devices = Device.objects.filter(customer__pk = customer.pk)
                        customer_devices.append((customer, devices))
                    template = 'customerservice/customerservice_customers.html'
                    context = dict()
                    context['customer_devices'] = customer_devices
                    return render(request, template, context)
                else:
                    return HttpResponse("Not found customer")
            else:
                return HttpResponse("Invalid form data")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_to_add_device(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        template = 'customerservice/customerservice_add_device.html'
        context = dict()
        if request.POST:    # it'll always be post but also better to check
            customer_id = request.POST.get('customer_id', None)
            request.session['customer_id'] = customer_id
            form = device_form.DeviceForm()
            context['form'] = form
            return render(request, template, context)
        else:
            return HttpResponse("This is not a post request")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_add_device(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        if request.POST:    # almost always will be a post request as well
            form = device_form.DeviceForm(request.POST)
            if form.is_valid():
                try:
                    f_c_d = form.cleaned_data
                    customer = Customer.objects.get(pk = request.session['customer_id'])
                    device = Device(model_name = f_c_d['model_name'], serial_number = f_c_d['serial_number'],\
                    purchase_date = f_c_d['purchase_date'],customer = customer)
                    device.save()
                except IntegrityError:
                    return HttpResponse("A device with that serial number already exists")
            return HttpResponse("Now it's a good job adding that device")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_add_customer(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        template = "customerservice/customerservice_add_customer.html"
        context = dict()
        if request.POST:
            form = customer_form.CustomerForm(request.POST)
            if form.is_valid():
                try:
                    f_c_d = form.cleaned_data
                    customer = Customer(first_name = f_c_d['first_name'], middle_name = f_c_d['middle_name'],\
                        last_name = f_c_d['last_name'], mobile_number = f_c_d['mobile_number'],\
                        land_phone_number = f_c_d['land_phone_number'], address_formated = f_c_d['address_formated'],\
                        longitude = f_c_d['longitude'], latitude = f_c_d['latitude'])
                    customer.save()
                    return HttpResponse("Customer successfully added")
                except IntegrityError:
                    return HttpResponse("customer with this phone or mobile already added")
            else:
                print(form.errors)
                return HttpResponse("Form data is invalid")
        else:
            form = customer_form.CustomerForm()
            context['form'] = form
        return render(request, template, context)
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_to_add_ticket(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        template = "customerservice/customerservice_add_ticket.html"
        context = dict()
        if request.POST:
            device_id = request.POST.get('device_id', None)
            if device_id:
                request.session['device_id'] = device_id
                form = ticket_form.TicketForm()
                context['form'] = form
                return render(request, template, context)
        else:
            return HttpResponse("not a post request")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_add_ticket(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        template = "customerservice/customerservice_add_ticket.html"
        context = dict()
        if request.POST:
            form = ticket_form.TicketForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                device_id = request.session.get('device_id', None)
                if device_id:
                    device = Device.objects.get(pk = device_id)
                    ticket = Ticket(problem_title = f_c_d['problem_title'], problem_description = f_c_d['problem_description'],\
                                status = f_c_d['status'], device_concerned = device)
                    ticket.save()
                    return HttpResponse("Good job adding this ticket")
                else:
                    return HttpResponse("There is no device to add a problem to")
            else:
                return HttpResponse("The form is invalid")
        else:
            form = ticket_form.TicketForm()
            context['form'] = form
        return render(request, template, context)
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_edit_customer(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        if request.GET:
            template = "customerservice/customerservice_edit_customer.html"
            context = dict()
            customer_id = int(request.GET['customer_id'])
            request.session['customer_id'] = customer_id
            customer = Customer.objects.get(pk = customer_id)
            data = {
                'first_name': customer.first_name,
                'middle_name': customer.middle_name,
                'last_name': customer.last_name,
                'mobile_number': customer.mobile_number,
                'land_phone_number': customer.land_phone_number,
                'address_formated': customer.address_formated,
                'longitude': customer.longitude,
                'latitude': customer.latitude
            }
            customer_edit_form = customer_form.CustomerForm(initial = data)
            context['form'] = customer_edit_form
            return render(request, template, context)
        elif request.POST:
            edit_form = customer_form.CustomerForm(request.POST)
            if edit_form.is_valid():
                f_c_d = edit_form.cleaned_data
                Customer.objects.filter(pk = request.session['customer_id']).update(**f_c_d)
                del request.session['customer_id']
                return HttpResponse("End the updating process")
            else:
                return HttpResponse("Form is not valid")

    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)


def customer_service_edit_device(request):
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        if request.GET:
            template = "customerservice/customerservice_edit_device.html"
            context = dict()
            device_id = int(request.GET['device_id'])
            request.session['device_id'] = device_id
            device = Device.objects.get(pk = device_id)
            data = {
                'model_name': device.model_name,
                'serial_number': device.serial_number,
                'purchase_date': device.purchase_date,
                'last_maintenance_date': device.last_maintenance_date
            }
            edit_device_form = device_form.DeviceForm(initial = data)
            context['form'] = edit_device_form
            return render(request, template, context)
        elif request.POST:
            edit_form = device_form.DeviceForm(request.POST)
            if edit_form.is_valid():
                f_c_d = edit_form.cleaned_data
                Device.objects.filter(pk = request.session['device_id']).update(**f_c_d)
                del request.session['device_id']
                return HttpResponse("End the updating device process")
            else:
                return HttpResponse("Form is not valid")
    else:
        response_redirect_url = reverse('customer_service_login')
        return HttpResponseRedirect(response_redirect_url)
