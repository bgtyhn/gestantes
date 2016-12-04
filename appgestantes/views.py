# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.core import serializers
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.views.generic import View
import re
from django.db.models import Q
from . import forms
from django.db.models.functions import Value
from django.db.models import CharField
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from .models import *


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query( query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class Index(ListView):
    model = Gestante
    template_name = 'appgestantes/pendientes.html'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        query_string = ''
        found_entries = None
        gestantes_pendientes = Cita.objects.all().filter(estado = 'Pendiente').only('gestante_id')
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            product_query = get_query(query_string, ['nombre', 'identificacion'])

            lista_gestantes = Gestante.objects.filter(product_query).filter(pk__in = gestantes_pendientes)
            context['search'] = self.request.GET['q']
        else:
            lista_gestantes = Gestante.objects.filter(pk__in = gestantes_pendientes)

        paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca')

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context

class Prioritarias(ListView):
    model = Gestante
    template_name = 'appgestantes/prioritarias.html'
    paginate_by = 15
    
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        query_string = ''
        found_entries = None
        gestantes_VIH = PrimerTrimestre.objects.all().filter(VIH = 'Reactivo').only('gestante_id')
        gestantes_VDRL = TercerTrimestre.objects.all().filter(VDRL = 'Reactivo').only('gestante_id')
        gestantes_toxoplasmosis_IGG = PrimerTrimestre.objects.all().filter(toxoplasmosis_IGG = 'IGG Positiva').only('gestante_id')
        gestantes_toxoplasmosis_IGM = PrimerTrimestre.objects.all().filter(toxoplasmosis_IGM = 'IGM Positiva').only('gestante_id')
        gestantes_hepatitisB = PrimerTrimestre.objects.all().filter(antigeno_hepatitisB = 'IGM Reactivo').only('gestante_id')
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            product_query = get_query(query_string, ['nombre', 'identificacion'])

            lista_gestantes = Gestante.objects.filter(product_query)
            gestantes_VIH = lista_gestantes.filter(pk__in = gestantes_VIH).annotate(causa=Value('VIH', output_field=CharField()))
            gestantes_VDRL = lista_gestantes.filter(pk__in = gestantes_VDRL).annotate(causa=Value('VDRL', output_field=CharField()))
            gestantes_toxoplasmosis_IGG = lista_gestantes.filter(pk__in = gestantes_toxoplasmosis_IGG).annotate(causa=Value('IGG', output_field=CharField()))
            gestantes_toxoplasmosis_IGM = lista_gestantes.filter(pk__in = gestantes_toxoplasmosis_IGM).annotate(causa=Value('IGM', output_field=CharField()))
            gestantes_hepatitisB = lista_gestantes.filter(pk__in = gestantes_hepatitisB).annotate(causa=Value('Hepatitis', output_field=CharField()))

            lista_gestantes = gestantes_VIH | gestantes_VDRL | gestantes_toxoplasmosis_IGM | gestantes_toxoplasmosis_IGG | gestantes_hepatitisB
            context['search'] = self.request.GET['q']
        else:
            gestantes_VIH_L = Gestante.objects.filter(pk__in = gestantes_VIH).annotate(causa=Value('VIH', output_field=CharField()))
            gestantes_VDRL_L = Gestante.objects.filter(pk__in = gestantes_VDRL).annotate(causa=Value('VDRL', output_field=CharField()))
            gestantes_toxoplasmosis_IGG_L = Gestante.objects.filter(pk__in = gestantes_toxoplasmosis_IGG).annotate(causa=Value('IGG', output_field=CharField()))
            gestantes_toxoplasmosis_IGM_L = Gestante.objects.filter(pk__in = gestantes_toxoplasmosis_IGM).annotate(causa=Value('IGM', output_field=CharField()))
            gestantes_hepatitisB_L = Gestante.objects.filter(pk__in = gestantes_hepatitisB).annotate(causa=Value('Hepatitis B', output_field=CharField()))

            lista_gestantes = gestantes_VIH_L | gestantes_VDRL_L | gestantes_toxoplasmosis_IGM_L | gestantes_toxoplasmosis_IGG_L | gestantes_hepatitisB_L

        paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca')

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context

class Completa(ListView):
    model = Gestante
    template_name = 'appgestantes/completa.html'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        query_string = ''
        found_entries = None
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            product_query = get_query(query_string, ['nombre', 'identificacion'])

            lista_gestantes = Gestante.objects.filter(product_query)
            context['search'] = self.request.GET['q']
        else:
            lista_gestantes = Gestante.objects.all()

        paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca')

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context

class Pasadas(ListView):
    model = Gestante
    template_name = 'appgestantes/pasadas.html'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        query_string = ''
        found_entries = None
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            product_query = get_query(query_string, ['nombre', 'identificacion'])

            lista_gestantes = Gestante.objects.filter(product_query).filter(Q(fecha_probable_parto=datetime().now().date()) | Q(fecha_probable_parto__gt=datetime().now().date()))
            context['search'] = self.request.GET['q']
        else:
            lista_gestantes = Gestante.objects.filter(Q(fecha_probable_parto=datetime.now().date()) | Q(fecha_probable_parto__gt=datetime.now().date()))

        paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca') 

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context


class Nueva(FormView):
    template_name = 'appgestantes/nueva_gestante.html'
    form_class = forms.GestanteForm
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(Nueva, self).get_context_data(**kwargs)
        context['opciones_captacion'] = CAPTACION
        return context

    def form_valid(self, form):
        
        print(form)
        gestante = Gestante(nombre = form.cleaned_data['nombre'],
            fecha_ingreso_programa = form.cleaned_data['fecha_ingreso_programa'],
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
            identificacion = form.cleaned_data['identificacion'],
            captacion = form.cleaned_data['captacion'],
            semana_ingreso = form.cleaned_data['semana_ingreso'],
            fecha_ultima_menstruacion = form.cleaned_data['fecha_ultima_menstruacion'],
            fecha_probable_parto = form.cleaned_data['fecha_probable_parto'],
            confiable = form.cleaned_data['confiable']
        )
        gestante.save()

        primer_control = PrimerControl(
            gestante = gestante,
            fecha_paraclinicos = form.cleaned_data['fecha_paraclinicos'],
            micronutrientes = form.cleaned_data['micronutrientes'],
            pretest_fecha = form.cleaned_data['pretest_fecha'],
            fecha_postest =form.cleaned_data['fecha_postest'],
            iami = form.cleaned_data['iami'],
            odontologia_fecha = form.cleaned_data['odontologia_fecha'],
            citologia_fecha = form.cleaned_data['citologia_fecha'],
            citologia_resultado = form.cleaned_data['citologia_resultado'],
            DPTa = form.cleaned_data['DPTa']
        )
        primer_control.save()
        self.success_url = self.success_url + str(gestante.pk) + '/'
        return super(Nueva, self).form_valid(form)

class Detalle(DetailView):
    model = Gestante
    template_name = 'appgestantes/detalle.html'

    def get_context_data(self, **kwargs):
        context = super(Detalle, self).get_context_data(**kwargs)
        gestante = context['object']
        try:
            context['primer_control'] = PrimerControl.objects.get(gestante_id = gestante.id)
        except ObjectDoesNotExist:
            context['primer_control'] = ""
        try:
            context['primer_trimestre'] = PrimerTrimestre.objects.get(gestante_id = gestante.id)
        except ObjectDoesNotExist:
            context['primer_trimestre'] = ""
        try:
            context['segundo_trimestre'] = SegundoTrimestre.objects.get(gestante_id = gestante.id)
        except ObjectDoesNotExist:
            context['segundo_trimestre'] = ""

        try:
            context['tercer_trimestre'] = TercerTrimestre.objects.get(gestante_id = gestante.id)
        except ObjectDoesNotExist:
            context['tercer_trimestre'] = ""

        context['citas'] = {}
        citasGestante = Cita.objects.filter(gestante_id = gestante.id)
        if citasGestante:
            context['citas']['fecha_parto'] = citasGestante.get(tipo_cita = 'Fecha parto')
            context['citas']['recien_nacido'] = citasGestante.get(tipo_cita = 'Recien nacido')
            context['citas']['puerperio'] = citasGestante.get(tipo_cita = 'Puerperio')
            context['citas']['crecimiento_desarrollo'] = citasGestante.get(tipo_cita = 'Crecimiento y Desarrollo')
            context['citas']['planificacion_familiar'] = citasGestante.get(tipo_cita = 'Planificación Familiar')

        return context

def editar_general(request):
    return render(request, 'appgestantes/forms_editar/editar_general.html')

def editar_primer_control(request):
    return render(request, 'appgestantes/forms_editar/editar_primer_control.html')

def editar_primer_trimestre(request):
    return render(request, 'appgestantes/forms_editar/editar_primer_trimestre.html')

def editar_segundo_trimestre(request):
    return render(request, 'appgestantes/forms_editar/editar_segundo_trimestre.html')

def editar_tercer_trimestre(request):
    return render(request, 'appgestantes/forms_editar/editar_tercer_trimestre.html')

def editar_citas(request):
    return render(request, 'appgestantes/forms_editar/editar_citas.html')