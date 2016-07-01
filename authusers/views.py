from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from authusers.forms.login_form import LoginForm
from authusers.models import CustomerServiceUser, DispatcherUser

# Create your views here.

def customer_service_login(request):
    template = 'login.html'
    context = dict()
    errors = list()
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            f_c_d = login_form.cleaned_data
            try:
                customerservice_user = CustomerServiceUser.objects.get(pk = f_c_d['username'])
                if customerservice_user.check_password(f_c_d['password']):
                    request.session['customerservice_user_id'] = f_c_d['username']
                    request.session['customer_service'] = True
                    response_redirect_url = reverse('customer_service_index', args = [f_c_d['username']])
                    return HttpResponseRedirect(response_redirect_url)
                else:
                    errors.append("Wrong password for this user name")
                    context['errors'] = errors
                    context['form'] = login_form    # to be able to hold the current form data
                    return render(request, template, context)
            except CustomerServiceUser.DoesNotExist:
                errors.append("This user name doesn't exist")
                context['errors'] = errors
                context['form'] = login_form     # to be able to hold the current form data
                return render(request, template, context)
        else:
            # need to do something else rather than just returning an HttpResponse object
            return HttpResponse("This is invalid data")

    else:
        context['form'] = LoginForm()
        return render(request,template, context)


def customer_service_logout(request):
    template = 'logout.html'
    context = dict()
    customerservice_user_id = request.session.get('customerservice_user_id', None)
    customer_service = request.session.get('customer_service', None)
    if customerservice_user_id and customer_service:
        del request.session['customerservice_user_id']
        del request.session['customer_service']
    else:
        return HttpResponse("Not logged in to logout")
    return render(request, template, context)


def dispatcher_login(request):
    template = "login.html"
    context = dict()
    errors = list()
    if request.POST:
        print("in post")
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            f_c_d = login_form.cleaned_data
            try:
                dispatcher_user = DispatcherUser.objects.get(pk = f_c_d['username'])
                if dispatcher_user.check_password(f_c_d['password']):
                    request.session['dispatcher_user_id'] = f_c_d['username']
                    request.session['dispatcher'] = True
                    response_redirect_url = reverse('dispatcher_index', args = [f_c_d['username']])
                    return HttpResponseRedirect(response_redirect_url)
                else:
                    errors.append("Wrong password for this user name")
                    context['errors'] = errors
                    context['form'] = login_form    # to be able to hold the current form data
                    return render(request, template, context)
            except DispatcherUser.DoesNotExist:
                errors.append("This user name doesn't exist")
                context['errors'] = errors
                context['form'] = login_form     # to be able to hold the current form data
                return render(request, template, context)
        else:
            # need to do something else rather than just returning an HttpResponse object
            return HttpResponse("This is invalid data")

    else:
        context['form'] = LoginForm()
        return render(request,template, context)


def dispatcher_logout(request):
    template = 'logout.html'
    context = dict()
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        del request.session['dispatcher_user_id']
        del request.session['dispatcher']
    else:
        return HttpResponse("not logged in to logout")
    return render(request, template, context)
