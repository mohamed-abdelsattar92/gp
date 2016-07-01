from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.urlresolvers import reverse


def dispatcher_index(request, username):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_index.html"
        context = dict()
        context['username'] = username
        return render(request, template, context)
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)
