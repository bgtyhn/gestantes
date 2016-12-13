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
        confiable = 'No'
        micronutrientes = 'No'
        DPTa = 'No'
        iami = 'No'
        if form.cleaned_data['confiable']:
            confiable = 'Si'

        if form.cleaned_data['micronutrientes']:
            micronutrientes = 'Si'

        if form.cleaned_data['DPTa']:
            DPTa = 'Si'

        if form.cleaned_data['iami']:
            iami = 'Si'
        gestante = Gestante(nombre = form.cleaned_data['nombre'],
            fecha_ingreso_programa = form.cleaned_data['fecha_ingreso_programa'],
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
            identificacion = form.cleaned_data['identificacion'],
            captacion = form.cleaned_data['captacion'],
            semana_ingreso = form.cleaned_data['semana_ingreso'],
            fecha_ultima_menstruacion = form.cleaned_data['fecha_ultima_menstruacion'],
            fecha_probable_parto = form.cleaned_data['fecha_probable_parto'],
            confiable = confiable
        )
        gestante.save()

        primer_control = PrimerControl(
            gestante = gestante,
            fecha_paraclinicos = form.cleaned_data['fecha_paraclinicos'],
            micronutrientes = micronutrientes,
            pretest_fecha = form.cleaned_data['pretest_fecha'],
            fecha_postest =form.cleaned_data['fecha_postest'],
            iami = iami,
            odontologia_fecha = form.cleaned_data['odontologia_fecha'],
            citologia_fecha = form.cleaned_data['citologia_fecha'],
            citologia_resultado = form.cleaned_data['citologia_resultado'],
            DPTa = DPTa
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
            context['citas']['fecha_parto'] = citasGestante.filter(tipo_cita = 'Fecha parto')
            context['citas']['recien_nacido'] = citasGestante.filter(tipo_cita = 'Recien nacido')
            context['citas']['puerperio'] = citasGestante.filter(tipo_cita = 'Puerperio')
            context['citas']['crecimiento_desarrollo'] = citasGestante.filter(tipo_cita = 'Crecimiento y Desarrollo')
            context['citas']['planificacion_familiar'] = citasGestante.filter(tipo_cita = 'Planificación Familiar')

        return context

class EditarGeneral(FormView):
    template_name = 'appgestantes/forms_editar/editar_general.html'
    form_class = forms.EditarGeneralForm
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(EditarGeneral, self).get_context_data(**kwargs)
        context['observaciones'] = Observacion.objects.filter(gestante_id = self.kwargs['gestante'])
        context['opciones_captacion'] = CAPTACION
        context['gestante_id'] = self.kwargs['gestante']
        context['nombre_gestante'] = Gestante.objects.get(id = self.kwargs['gestante']).nombre
        return context

    def form_valid(self, form):
        confiable = 'No'
        if form.cleaned_data['confiable']:
            confiable = 'Si'
        g = Gestante.objects.get(id = self.kwargs['gestante'])
        g.nombre = form.cleaned_data['nombre']
        g.fecha_ingreso_programa = form.cleaned_data['fecha_ingreso_programa']
        g.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        g.identificacion = form.cleaned_data['identificacion']
        g.captacion = form.cleaned_data['captacion']
        g.semana_ingreso = form.cleaned_data['semana_ingreso']
        g.fecha_ultima_menstruacion = form.cleaned_data['fecha_ultima_menstruacion']
        g.fecha_probable_parto = form.cleaned_data['fecha_probable_parto']
        g.confiable = confiable
        g.save()

        Observacion.objects.filter(gestante_id = g.id).delete()

        for o in self.request.POST.getlist("observacion"):
            if o:
                Observacion.objects.create(gestante=g, texto=o)

        self.success_url = self.success_url + str(g.pk) + '/'

        return super(EditarGeneral, self).form_valid(form)

    def get_initial(self):
        initial = super(EditarGeneral, self).get_initial()

        try:
            gestante = Gestante.objects.get(id = self.kwargs['gestante'])
            initial['nombre'] = gestante.nombre
            initial['fecha_probable_parto'] = gestante.fecha_probable_parto.strftime('%Y-%m-%d')
            initial['identificacion'] = gestante.identificacion
            initial['confiable'] = gestante.confiable
            initial['fecha_nacimiento'] = gestante.fecha_nacimiento.strftime('%Y-%m-%d')
            initial['semana_ingreso'] = gestante.semana_ingreso
            initial['captacion'] = gestante.captacion
            initial['fecha_ultima_menstruacion'] = gestante.fecha_ultima_menstruacion.strftime('%Y-%m-%d')
            initial['fecha_ingreso_programa'] = gestante.fecha_ingreso_programa.strftime('%Y-%m-%d')
            print(initial)
            return initial
        except ObjectDoesNotExist:
            return initial

class EditarPrimerControl(FormView):
    template_name = 'appgestantes/forms_editar/editar_primer_control.html'
    form_class = forms.EditarPrimerControl
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(EditarPrimerControl, self).get_context_data(**kwargs)
        context['riesgos'] = Riesgo.objects.filter(primerControl = self.kwargs['control'])
        context['gestante_id'] = self.kwargs['gestante']
        context['nombre_gestante'] = Gestante.objects.get(id = self.kwargs['gestante']).nombre
        return context

    def form_valid(self, form):
        micronutrientes = 'No'
        DPTa = 'No'
        iami = 'No'
        if form.cleaned_data['micronutrientes']:
            micronutrientes = 'Si'

        if form.cleaned_data['DPTa']:
            DPTa = 'Si'

        if form.cleaned_data['iami']:
            iami = 'Si'
        pc = PrimerControl.objects.get(id = self.kwargs['control'])
        pc.fecha_paraclinicos = form.cleaned_data['fecha_paraclinicos']
        pc.micronutrientes = micronutrientes
        pc.pretest_fecha = form.cleaned_data['pretest_fecha']
        pc.fecha_postest = form.cleaned_data['fecha_postest']
        pc.iami = iami
        pc.odontologia_fecha = form.cleaned_data['odontologia_fecha']
        pc.citologia_fecha = form.cleaned_data['citologia_fecha']
        pc.citologia_resultado = form.cleaned_data['citologia_resultado']
        pc.DPTa = DPTa
        pc.save()

        Riesgo.objects.filter(primerControl_id = self.kwargs['gestante']).delete()

        for r in self.request.POST.getlist("texto_rie"):
            if r:
                Riesgo.objects.create(primerControl=pc, motivo=r)

        self.success_url = self.success_url + str(self.kwargs['gestante']) + '/#tab_primer_control'

        return super(EditarPrimerControl, self).form_valid(form)

    def get_initial(self):
        initial = super(EditarPrimerControl, self).get_initial()

        try:
            pc = PrimerControl.objects.get(id = self.kwargs['control'])
            initial['fecha_paraclinicos'] = pc.fecha_paraclinicos.strftime('%Y-%m-%d')
            initial['micronutrientes'] = pc.micronutrientes
            initial['pretest_fecha'] = pc.pretest_fecha.strftime('%Y-%m-%d')
            initial['fecha_postest'] = pc.fecha_postest.strftime('%Y-%m-%d')
            initial['iami'] = pc.iami
            initial['odontologia_fecha'] = pc.odontologia_fecha.strftime('%Y-%m-%d')
            initial['citologia_fecha'] = pc.citologia_fecha.strftime('%Y-%m-%d')
            initial['citologia_resultado'] = pc.citologia_resultado
            initial['DPTa'] = pc.DPTa
            print(initial)
            return initial
        except ObjectDoesNotExist:
            return initial

class EditarPrimerTrimestre(FormView):
    template_name = 'appgestantes/forms_editar/editar_primer_trimestre.html'
    form_class = forms.EditarPrimerControl
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(EditarPrimerTrimestre, self).get_context_data(**kwargs)
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            primer_trimestre = PrimerTrimestre.objects.get(gestante_id = gestante.id)
            context['lista_motivosCH'] = ListaMotivosCHPT.objects.filter(primer_trimestre = primer_trimestre)
            context['lista_motivosFR'] = ListaMotivosFrotisPT.objects.filter(primer_trimestre = primer_trimestre)
        except ObjectDoesNotExist:
            context['lista_motivosCH'] = []
            context['lista_motivosFR'] = []

        context['gestante_id'] = self.kwargs['gestante']
        context['nombre_gestante'] = gestante.nombre
        context['opciones_parcial_horina'] = PARCIAL_ORINA
        context['opciones_cuadro_hematico'] = CUADRO_HEMATICO
        context['opciones_VDRL'] = VDRL
        context['opciones_VIH'] = VIH
        context['opciones_frotis'] = FROTIS
        context['si_opciones'] = SI_OPCIONES
        context['opciones_antigeno'] = ANTIGENO
        context['opciones_toxoplasmosis_igg'] = TOXOPLASMOSIS_IGG
        context['opciones_toxoplasmosis_igm'] = TOXOPLASMOSIS_IGM

    def form_valid(self, form):
        micronutrientes = 'No'
        if form.cleaned_data['micronutrientes']:
            micronutrientes = 'Si'

        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            primer_trimestre = PrimerTrimestre.objects.get(gestante_id = gestante.id)
            primer_trimestre.cuadro_hematico = form.cleaned_data['cuadro_hematico']
            primer_trimestre.parcial_orina = form.cleaned_data['parcial_orina']
            primer_trimestre.RH = form.cleaned_data['RH']
            primer_trimestre.VDRL = form.cleaned_data['VDRL']
            primer_trimestre.VIH = form.cleaned_data['VIH']
            primer_trimestre.frotis_fecha = form.cleaned_data['frotis_fecha']
            primer_trimestre.frotis_tipo = form.cleaned_data['frotis_tipo']
            primer_trimestre.factores_riesgo_diabetes_gestacional = form.cleaned_data['factores_riesgo_diabetes_gestacional']
            primer_trimestre.estado_factores_diabetes = form.cleaned_data['estado_factores_diabetes']
            primer_trimestre.fecha_factores_diabetes = form.cleaned_data['fecha_factores_diabetes']
            primer_trimestre.numero_factores_diabetes = form.cleaned_data['numero_factores_diabetes']
            primer_trimestre.ecografia_fecha = form.cleaned_data['ecografia_fecha']
            primer_trimestre.ecografia_semanas = form.cleaned_data['ecografia_semanas']
            primer_trimestre.micronutrientes = form.cleaned_data['micronutrientes']
            primer_trimestre.antigeno_hepatitisB = form.cleaned_data['antigeno_hepatitisB']
            primer_trimestre.toxoplasmosis_IGG = form.cleaned_data['toxoplasmosis_IGG']
            primer_trimestre.toxoplasmosis_IGM = form.cleaned_data['toxoplasmosis_IGM']
        except ObjectDoesNotExist:
            primer_trimestre = PrimerTrimestre(cuadro_hematico = form.cleaned_data['cuadro_hematico'],
                parcial_orina = form.cleaned_data['parcial_orina'],
                RH = form.cleaned_data['RH'],
                VDRL = form.cleaned_data['VDRL'],
                VIH = form.cleaned_data['VIH'],
                frotis_fecha = form.cleaned_data['frotis_fecha'],
                frotis_tipo = form.cleaned_data['frotis_tipo'],
                factores_riesgo_diabetes_gestacional = form.cleaned_data['factores_riesgo_diabetes_gestacional'],
                estado_factores_diabetes = form.cleaned_data['estado_factores_diabetes'],
                fecha_factores_diabetes = form.cleaned_data['fecha_factores_diabetes'],
                numero_factores_diabetes = form.cleaned_data['numero_factores_diabetes'],
                ecografia_fecha = form.cleaned_data['ecografia_fecha'],
                ecografia_semanas = form.cleaned_data['ecografia_semanas'],
                micronutrientes = form.cleaned_data['micronutrientes'],
                antigeno_hepatitisB = form.cleaned_data['antigeno_hepatitisB'],
                toxoplasmosis_IGG = form.cleaned_data['toxoplasmosis_IGG'],
                toxoplasmosis_IGM = form.cleaned_data['toxoplasmosis_IGM'],
            )
        primer_trimestre.save()

        ListaMotivosCHPT.objects.filter(primer_trimestre_id = primer_trimestre.id).delete()
        ListaMotivosFrotisPT.objects.filter(primer_trimestre_id = primer_trimestre.id).delete()

        for m in self.request.POST.getlist("motivo_hematico"):
            if m:
                ListaMotivosCHPT.objects.create(primer_trimestre=primer_trimestre, motivo=m)

        for m in self.request.POST.getlist("motivo_frotis"):
            if m:
                ListaMotivosFrotisPT.objects.create(primer_trimestre=primer_trimestre, motivo=m)

        self.success_url = self.success_url + str(self.kwargs['gestante']) + '/#tab_primer_trimestre"'

        return super(EditarPrimerTrimestre, self).form_valid(form)


    def get_initial(self):
        initial = super(EditarPrimerTrimestre, self).get_initial()
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            primer_trimestre = PrimerTrimestre.objects.get(gestante_id = gestante.id)
            initial['cuadro_hematico'] = primer_trimestre.cuadro_hematico
            initial['parcial_orina'] = primer_trimestre.parcial_orina
            initial['RH'] = primer_trimestre.RH
            initial['VDRL'] = primer_trimestre.VDRL
            initial['VIH'] = primer_trimestre.VIH
            initial['frotis_fecha'] = primer_trimestre.frotis_fecha.strftime('%Y-%m-%d')
            initial['frotis_tipo'] = primer_trimestre.frotis_tipo
            initial['factores_riesgo_diabetes_gestacional'] = primer_trimestre.factores_riesgo_diabetes_gestacional
            initial['estado_factores_diabetes'] = primer_trimestre.estado_factores_diabetes
            initial['fecha_factores_diabetes'] = primer_trimestre.fecha_factores_diabetes.strftime('%Y-%m-%d')
            initial['numero_factores_diabetes'] = primer_trimestre.numero_factores_diabetes
            initial['ecografia_fecha'] = primer_trimestre.ecografia_fecha.strftime('%Y-%m-%d')
            initial['ecografia_semanas'] = primer_trimestre.ecografia_semanas
            initial['micronutrientes'] = primer_trimestre.micronutrientes
            initial['antigeno_hepatitisB'] = primer_trimestre.antigeno_hepatitisB
            initial['toxoplasmosis_IGG'] = primer_trimestre.toxoplasmosis_IGG
            initial['toxoplasmosis_IGM'] = primer_trimestre.toxoplasmosis_IGM
            print(initial)
            return initial
        except ObjectDoesNotExist:
            return initial

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
