from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from authusers.forms.login_form import LoginForm
from authusers.models import CustomerServiceUser

# Create your views here.

def customer_service_login(request):
    template = 'customerservice/customerservice_login.html'
    context = dict()
    errors = list()
    context['form'] = LoginForm()

    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            form_cleaned_data = login_form.cleaned_data
            try:
                customerservice_user = CustomerServiceUser.objects.get(pk = form_cleaned_data['username'])
                if customerservice_user.check_password(form_cleaned_data['password']):
                    request.session['user_id'] = form_cleaned_data['username']
                    response_redirect_url = reverse('customer_service_index', args = [form_cleaned_data['username']])
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
        return render(request,template, context)


def customer_service_logout(request):
    template = 'customerservice/customerservice_logout.html'
    context = dict()
    user_id = request.session.get('user_id', None)
    if user_id:
        del request.session['user_id']
    return render(request, template, context)
