from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    template = 'index.html'
    context = dict()
    return render(request, template, context)
