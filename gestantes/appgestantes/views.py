from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    template = loader.get_template('appgestantes/pendientes.html')
    context = {}
    return HttpResponse(template.render(context, request))

def prioritarias(request):
    template = loader.get_template('appgestantes/prioritarias.html')
    context = {}
    return HttpResponse(template.render(context, request))

def completa(request):
    template = loader.get_template('appgestantes/completa.html')
    context = {}
    return HttpResponse(template.render(context, request))

def pasadas(request):
    template = loader.get_template('appgestantes/pasadas.html')
    context = {}
    return HttpResponse(template.render(context, request))

def nueva(request):
    template = loader.get_template('appgestantes/nueva_gestante.html')
    context = {}
    return HttpResponse(template.render(context, request))

def detalle(request):
    template = loader.get_template('appgestantes/detalle.html')
    context = {}
    return HttpResponse(template.render(context, request))