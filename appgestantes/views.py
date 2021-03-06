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
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            product_query = get_query(query_string, ['nombre', 'identificacion', 'EPS'])

            lista_gestantes = Gestante.objects.filter(product_query).filter(Q(fecha_probable_parto__gt=datetime.now().date()))
            context['search'] = self.request.GET['q']
        else:
            lista_gestantes = Gestante.objects.filter(Q(fecha_probable_parto__gt=datetime.now().date()))

        context['lista_gestantes'] = lista_gestantes

        '''paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca')

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes'''
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

            #lista_gestantes = gestantes_VIH | gestantes_VDRL | gestantes_toxoplasmosis_IGM | gestantes_toxoplasmosis_IGG | gestantes_hepatitisB
            context['search'] = self.request.GET['q']
        else:
            gestantes_VIH = Gestante.objects.filter(pk__in = gestantes_VIH).annotate(causa=Value('VIH', output_field=CharField()))
            gestantes_VDRL = Gestante.objects.filter(pk__in = gestantes_VDRL).annotate(causa=Value('VDRL', output_field=CharField()))
            gestantes_toxoplasmosis_IGG = Gestante.objects.filter(pk__in = gestantes_toxoplasmosis_IGG).annotate(causa=Value('IGG', output_field=CharField()))
            gestantes_toxoplasmosis_IGM = Gestante.objects.filter(pk__in = gestantes_toxoplasmosis_IGM).annotate(causa=Value('IGM', output_field=CharField()))
            gestantes_hepatitisB = Gestante.objects.filter(pk__in = gestantes_hepatitisB).annotate(causa=Value('Hepatitis B', output_field=CharField()))

            #lista_gestantes = gestantes_VIH_L | gestantes_VDRL_L | gestantes_toxoplasmosis_IGM_L | gestantes_toxoplasmosis_IGG_L | gestantes_hepatitisB_L

        lista_gestantes = []
        lista_gestantes.extend(gestantes_VIH)
        lista_gestantes.extend(gestantes_VDRL)
        lista_gestantes.extend(gestantes_toxoplasmosis_IGG)
        lista_gestantes.extend(gestantes_toxoplasmosis_IGM)
        lista_gestantes.extend(gestantes_hepatitisB)
        print(gestantes_VIH)
        print(gestantes_VDRL)
        print(gestantes_toxoplasmosis_IGG)
        print(gestantes_toxoplasmosis_IGM)
        print(gestantes_hepatitisB)
        print(lista_gestantes)

        context['lista_gestantes'] = lista_gestantes

        return context

        '''paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca')

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context'''

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

        context['lista_gestantes'] = lista_gestantes
        return context
        '''paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca')

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context'''

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

            lista_gestantes = Gestante.objects.filter(product_query)
            lista_gestantes = lista_gestantes.filter(Q(fecha_probable_parto=datetime.now().date()) | Q(fecha_probable_parto__lt=datetime.now().date()))
            context['search'] = self.request.GET['q']
        else:
            lista_gestantes = Gestante.objects.filter(Q(fecha_probable_parto=datetime.now().date()) | Q(fecha_probable_parto__lt=datetime.now().date()))

        context['lista_gestantes'] = lista_gestantes
        return context
        '''paginator = Paginator(lista_gestantes, self.paginate_by)
        print('aca') 

        page = self.request.GET.get('page')
        try:
            gestantes = paginator.page(page)
        except PageNotAnInteger:
            gestantes = paginator.page(1)
        except EmptyPage:
            gestantes = paginator.page(paginator.num_pages)
        context['lista_gestantes'] = gestantes
        return context'''


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
            edad = form.cleaned_data['edad'],
            identificacion = form.cleaned_data['identificacion'],
            captacion = form.cleaned_data['captacion'],
            semana_ingreso = form.cleaned_data['semana_ingreso'],
            fecha_ultima_menstruacion = form.cleaned_data['fecha_ultima_menstruacion'],
            fecha_probable_parto = form.cleaned_data['fecha_probable_parto'],
            EPS = form.cleaned_data['EPS'],
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
            cfp = citasGestante.filter(tipo_cita = 'Fechaparto')
            if cfp:
                context['citas']['fecha_parto'] = cfp[0]
            crn = citasGestante.filter(tipo_cita = 'Reciennacido')
            if crn:
                context['citas']['recien_nacido'] = crn[0]
            cp = citasGestante.filter(tipo_cita = 'Puerperio')
            if cp:
                context['citas']['puerperio'] = cp[0]
            ccd = citasGestante.filter(tipo_cita = 'CrecimientoyDesarrollo')
            if ccd:
                context['citas']['crecimiento_desarrollo'] = ccd[0]
            cpf = citasGestante.filter(tipo_cita = 'PlanificacionFamiliar')
            if cpf:
                context['citas']['planificacion_familiar'] = cpf[0]
            print(context)

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
        g.edad = form.cleaned_data['edad']
        g.identificacion = form.cleaned_data['identificacion']
        g.captacion = form.cleaned_data['captacion']
        g.semana_ingreso = form.cleaned_data['semana_ingreso']
        g.fecha_ultima_menstruacion = form.cleaned_data['fecha_ultima_menstruacion']
        g.fecha_probable_parto = form.cleaned_data['fecha_probable_parto']
        g.EPS = form.cleaned_data['EPS']
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
            if gestante.fecha_probable_parto:
                initial['fecha_probable_parto'] = gestante.fecha_probable_parto.strftime('%Y-%m-%d')
            initial['identificacion'] = gestante.identificacion
            initial['confiable'] = gestante.confiable
            initial['edad'] = gestante.edad
            initial['semana_ingreso'] = gestante.semana_ingreso
            initial['captacion'] = gestante.captacion
            initial['EPS'] = gestante.EPS
            if gestante.fecha_ultima_menstruacion:
                initial['fecha_ultima_menstruacion'] = gestante.fecha_ultima_menstruacion.strftime('%Y-%m-%d')
            if gestante.fecha_ingreso_programa:
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
            if pc.fecha_paraclinicos:
                initial['fecha_paraclinicos'] = pc.fecha_paraclinicos.strftime('%Y-%m-%d')
            initial['micronutrientes'] = pc.micronutrientes
            if pc.pretest_fecha:
                initial['pretest_fecha'] = pc.pretest_fecha.strftime('%Y-%m-%d')
            if pc.fecha_postest:
                initial['fecha_postest'] = pc.fecha_postest.strftime('%Y-%m-%d')
            initial['iami'] = pc.iami
            if pc.odontologia_fecha:
                initial['odontologia_fecha'] = pc.odontologia_fecha.strftime('%Y-%m-%d')
            if pc.citologia_fecha:
                initial['citologia_fecha'] = pc.citologia_fecha.strftime('%Y-%m-%d')
            initial['citologia_resultado'] = pc.citologia_resultado
            initial['DPTa'] = pc.DPTa
            print(initial)
            return initial
        except ObjectDoesNotExist:
            return initial

class EditarPrimerTrimestre(FormView):
    template_name = 'appgestantes/forms_editar/editar_primer_trimestre.html'
    form_class = forms.EditarPrimerTrimestre
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
        return context

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
            primer_trimestre.micronutrientes = micronutrientes
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
                micronutrientes = micronutrientes,
                antigeno_hepatitisB = form.cleaned_data['antigeno_hepatitisB'],
                toxoplasmosis_IGG = form.cleaned_data['toxoplasmosis_IGG'],
                toxoplasmosis_IGM = form.cleaned_data['toxoplasmosis_IGM'],
            )
        primer_trimestre.gestante = gestante
        primer_trimestre.save()

        ListaMotivosCHPT.objects.filter(primer_trimestre_id = primer_trimestre.id).delete()
        ListaMotivosFrotisPT.objects.filter(primer_trimestre_id = primer_trimestre.id).delete()

        for m in self.request.POST.getlist("motivo_hematico"):
            if m:
                ListaMotivosCHPT.objects.create(primer_trimestre=primer_trimestre, motivo=m)

        for m in self.request.POST.getlist("motivo_frotis"):
            if m:
                ListaMotivosFrotisPT.objects.create(primer_trimestre=primer_trimestre, motivo=m)

        self.success_url = self.success_url + str(self.kwargs['gestante']) + '/#tab_primer_trimestre'

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
            if primer_trimestre.frotis_fecha:
                initial['frotis_fecha'] = primer_trimestre.frotis_fecha.strftime('%Y-%m-%d')
            initial['frotis_tipo'] = primer_trimestre.frotis_tipo
            initial['factores_riesgo_diabetes_gestacional'] = primer_trimestre.factores_riesgo_diabetes_gestacional
            initial['estado_factores_diabetes'] = primer_trimestre.estado_factores_diabetes
            if primer_trimestre.fecha_factores_diabetes:
                initial['fecha_factores_diabetes'] = primer_trimestre.fecha_factores_diabetes.strftime('%Y-%m-%d')
            initial['numero_factores_diabetes'] = primer_trimestre.numero_factores_diabetes
            if primer_trimestre.ecografia_fecha:
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

class EditarSegundoTrimestre(FormView):
    template_name = 'appgestantes/forms_editar/editar_segundo_trimestre.html'
    form_class = forms.EditarSegundoTrimestre
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(EditarSegundoTrimestre, self).get_context_data(**kwargs)
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])

        context['gestante_id'] = self.kwargs['gestante']
        context['nombre_gestante'] = gestante.nombre
        context['opciones_parcial_horina'] = PARCIAL_ORINA
        context['opciones_VDRL'] = VDRL
        context['opciones_frotis'] = FROTIS
        context['si_opciones'] = SI_OPCIONES
        return context

    def form_valid(self, form):
        micronutrientes = 'No'
        if form.cleaned_data['micronutrientes']:
            micronutrientes = 'Si'

        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            segundo_trimestre = SegundoTrimestre.objects.get(gestante_id = gestante.id)
            segundo_trimestre.VDRL = form.cleaned_data['VDRL']
            segundo_trimestre.parcial_horina = form.cleaned_data['parcial_horina']
            segundo_trimestre.factores_riesgo_diabetes_gestacional = form.cleaned_data['factores_riesgo_diabetes_gestacional']
            segundo_trimestre.fecha_factores_riesgo = form.cleaned_data['fecha_factores_riesgo']
            segundo_trimestre.estado_factores_diabetes = form.cleaned_data['estado_factores_diabetes']
            segundo_trimestre.fecha_factores_diabetes = form.cleaned_data['fecha_factores_diabetes']
            segundo_trimestre.numero_factores_diabetes = form.cleaned_data['numero_factores_diabetes']
            segundo_trimestre.ecografia_fecha = form.cleaned_data['ecografia_fecha']
            segundo_trimestre.ecografia_semanas = form.cleaned_data['ecografia_semanas']
            segundo_trimestre.micronutrientes = micronutrientes
        except ObjectDoesNotExist:
            segundo_trimestre = SegundoTrimestre(VDRL = form.cleaned_data['VDRL'],
                parcial_horina = form.cleaned_data['parcial_horina'],
                factores_riesgo_diabetes_gestacional = form.cleaned_data['factores_riesgo_diabetes_gestacional'],
                fecha_factores_riesgo = form.cleaned_data['fecha_factores_riesgo'],
                estado_factores_diabetes = form.cleaned_data['estado_factores_diabetes'],
                fecha_factores_diabetes = form.cleaned_data['fecha_factores_diabetes'],
                numero_factores_diabetes = form.cleaned_data['numero_factores_diabetes'],
                ecografia_fecha = form.cleaned_data['ecografia_fecha'],
                ecografia_semanas = form.cleaned_data['ecografia_semanas'],
                micronutrientes = micronutrientes,
            )
        segundo_trimestre.gestante = gestante 
        segundo_trimestre.save()

        self.success_url = self.success_url + str(self.kwargs['gestante']) + '/#tab_segundo_trimestre'

        return super(EditarSegundoTrimestre, self).form_valid(form)


    def get_initial(self):
        initial = super(EditarSegundoTrimestre, self).get_initial()
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            segundo_trimestre = SegundoTrimestre.objects.get(gestante_id = gestante.id)
            initial['VDRL'] = segundo_trimestre.VDRL
            initial['parcial_horina'] = segundo_trimestre.parcial_horina
            initial['factores_riesgo_diabetes_gestacional'] = segundo_trimestre.factores_riesgo_diabetes_gestacional
            initial['fecha_factores_riesgo'] = segundo_trimestre.fecha_factores_riesgo
            initial['estado_factores_diabetes'] = segundo_trimestre.estado_factores_diabetes
            if segundo_trimestre.fecha_factores_diabetes:
                initial['fecha_factores_diabetes'] = segundo_trimestre.fecha_factores_diabetes.strftime('%Y-%m-%d')
            initial['numero_factores_diabetes'] = segundo_trimestre.numero_factores_diabetes
            if segundo_trimestre.ecografia_fecha:
                initial['ecografia_fecha'] = segundo_trimestre.ecografia_fecha.strftime('%Y-%m-%d')
            initial['ecografia_semanas'] = segundo_trimestre.ecografia_semanas
            initial['micronutrientes'] = segundo_trimestre.micronutrientes
            print(initial)
            return initial
        except ObjectDoesNotExist:
            return initial

class EditarTercerTrimestre(FormView):
    template_name = 'appgestantes/forms_editar/editar_tercer_trimestre.html'
    form_class = forms.EditarTercerTrimestre
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(EditarTercerTrimestre, self).get_context_data(**kwargs)
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])

        context['gestante_id'] = self.kwargs['gestante']
        context['nombre_gestante'] = gestante.nombre
        context['opciones_parcial_orina'] = PARCIAL_ORINA
        context['opciones_VDRL'] = VDRL
        context['opciones_VIH'] = VIH
        return context

    def form_valid(self, form):
        micronutrientes = 'No'
        if form.cleaned_data['micronutrientes']:
            micronutrientes = 'Si'

        factores_riesgo_VIH = 'No'
        if form.cleaned_data['factores_riesgo_VIH']:
            factores_riesgo_VIH = 'Si'
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            tercer_trimestre = TercerTrimestre.objects.get(gestante_id = gestante.id)
            tercer_trimestre.VDRL = form.cleaned_data['VDRL']
            tercer_trimestre.parcial_orina = form.cleaned_data['parcial_orina']
            tercer_trimestre.factores_riesgo_VIH  = factores_riesgo_VIH
            tercer_trimestre.fecha_VIH = form.cleaned_data['fecha_VIH']
            tercer_trimestre.reactivo_VIH = form.cleaned_data['reactivo_VIH']
            tercer_trimestre.ecografia_unica_semanas = form.cleaned_data['ecografia_unica_semanas']
            tercer_trimestre.ecografia_unica_fecha = form.cleaned_data['ecografia_unica_fecha']
            tercer_trimestre.micronutrientes = micronutrientes
        except ObjectDoesNotExist:
            tercer_trimestre = TercerTrimestre(VDRL = form.cleaned_data['VDRL'],
                parcial_orina = form.cleaned_data['parcial_orina'],
                factores_riesgo_VIH  = factores_riesgo_VIH,
                fecha_VIH = form.cleaned_data['fecha_VIH'],
                reactivo_VIH = form.cleaned_data['reactivo_VIH'],
                ecografia_unica_semanas = form.cleaned_data['ecografia_unica_semanas'],
                ecografia_unica_fecha = form.cleaned_data['ecografia_unica_fecha'],
                micronutrientes = micronutrientes
            )
        tercer_trimestre.gestante = gestante 
        tercer_trimestre.save()

        self.success_url = self.success_url + str(self.kwargs['gestante']) + '/#tab_tercer_trimestre'

        return super(EditarTercerTrimestre, self).form_valid(form)


    def get_initial(self):
        initial = super(EditarTercerTrimestre, self).get_initial()
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            tercer_trimestre = TercerTrimestre.objects.get(gestante_id = gestante.id)
            initial['VDRL'] = tercer_trimestre.VDRL
            initial['parcial_orina'] = tercer_trimestre.parcial_orina
            initial['factores_riesgo_VIH'] = tercer_trimestre.factores_riesgo_VIH
            if tercer_trimestre.fecha_VIH:
                initial['fecha_VIH'] = tercer_trimestre.fecha_VIH.strftime('%Y-%m-%d')
            initial['reactivo_VIH'] = tercer_trimestre.reactivo_VIH
            initial['ecografia_unica_semanas'] = tercer_trimestre.ecografia_unica_semanas
            if tercer_trimestre.ecografia_unica_fecha:
                initial['ecografia_unica_fecha'] = tercer_trimestre.ecografia_unica_fecha.strftime('%Y-%m-%d')
            initial['micronutrientes'] = tercer_trimestre.micronutrientes
            print(initial)
            return initial
        except ObjectDoesNotExist:
            return initial

class EditarCitas(FormView):
    template_name = 'appgestantes/forms_editar/editar_citas.html'
    form_class = forms.EditarCitas
    success_url = '/detalle/'

    def get_context_data(self, **kwargs):
        context = super(EditarCitas, self).get_context_data(**kwargs)
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        context['gestante_id'] = self.kwargs['gestante']
        context['nombre_gestante'] = gestante.nombre
        context['opciones_estado'] = ESTADO_CITA
        return context

    def form_valid(self, form):
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            cita_parto = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'Fechaparto')
            cita_parto.estado = form.cleaned_data["estadoFechaparto"]
            cita_parto.fecha = form.cleaned_data["fechaFechaparto"]
            cita_parto.info_adicional = form.cleaned_data["info_adicionalFechaparto"]
        except ObjectDoesNotExist:
            cita_parto = Cita(tipo_cita = 'Fechaparto',
                estado = form.cleaned_data["estadoFechaparto"],
                fecha = form.cleaned_data["fechaFechaparto"],
                info_adicional = form.cleaned_data["info_adicionalFechaparto"]
            )
        cita_parto.gestante = gestante
        cita_parto.save()

        try:
            cita_recien_nacido = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'Reciennacido')
            cita_recien_nacido.estado = form.cleaned_data["estadoReciennacido"]
            cita_recien_nacido.fecha = form.cleaned_data["fechaReciennacido"]
            cita_recien_nacido.info_adicional = form.cleaned_data["info_adicionalReciennacido"]
        except ObjectDoesNotExist:
            cita_recien_nacido = Cita(tipo_cita = 'Reciennacido',
                estado = form.cleaned_data["estadoReciennacido"],
                fecha = form.cleaned_data["fechaReciennacido"],
                info_adicional = form.cleaned_data["info_adicionalReciennacido"]
            )

        cita_recien_nacido.gestante = gestante
        cita_recien_nacido.save()
        try:
            cita_puerperio = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'Puerperio')
            cita_puerperio.estado = form.cleaned_data["estadoPuerperio"]
            cita_puerperio.fecha = form.cleaned_data["fechaPuerperio"]
            cita_puerperio.info_adicional = form.cleaned_data["info_adicionalPuerperio"]
        except ObjectDoesNotExist:
            cita_puerperio = Cita(tipo_cita = 'Puerperio',
                estado = form.cleaned_data["estadoPuerperio"],
                fecha = form.cleaned_data["fechaPuerperio"],
                info_adicional = form.cleaned_data["info_adicionalPuerperio"]
            )

        cita_puerperio.gestante = gestante
        cita_puerperio.save()
        try:
            cita_crecimiento = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'CrecimientoyDesarrollo')
            cita_crecimiento.estado = form.cleaned_data["estadoCrecimientoyDesarrollo"]
            cita_crecimiento.fecha = form.cleaned_data["fechaCrecimientoyDesarrollo"]
            cita_crecimiento.info_adicional = form.cleaned_data["info_adicionalCrecimientoyDesarrollo"]
        except ObjectDoesNotExist:
            cita_crecimiento = Cita(tipo_cita = 'CrecimientoyDesarrollo',
                estado = form.cleaned_data["estadoCrecimientoyDesarrollo"],
                fecha = form.cleaned_data["fechaCrecimientoyDesarrollo"],
                info_adicional = form.cleaned_data["info_adicionalCrecimientoyDesarrollo"]
            )
        cita_crecimiento.gestante = gestante
        cita_crecimiento.save()

        try:
            cita_planificacion = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'PlanificacionFamiliar')
            cita_planificacion.estado =form.cleaned_data["estadoPlanificacionFamiliar"]
            cita_planificacion.fecha = form.cleaned_data["fechaPlanificacionFamiliar"]
            cita_planificacion.info_adicional = form.cleaned_data["info_adicionalPlanificacionFamiliar"]
        except ObjectDoesNotExist:
            cita_planificacion = Cita(tipo_cita = 'PlanificacionFamiliar',
                estado = form.cleaned_data["estadoPlanificacionFamiliar"],
                fecha =form.cleaned_data["fechaPlanificacionFamiliar"],
                info_adicional = form.cleaned_data["info_adicionalPlanificacionFamiliar"]
            )

        cita_planificacion.gestante = gestante
        cita_planificacion.save()


        self.success_url = self.success_url + str(self.kwargs['gestante']) + '/#tab_citas'

        return super(EditarCitas, self).form_valid(form)


    def get_initial(self):
        initial = super(EditarCitas, self).get_initial()
        gestante = Gestante.objects.get(id = self.kwargs['gestante'])
        try:
            cita_parto = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'Fechaparto')
            initial["estadoFechaparto"] = cita_parto.estado 
            if cita_parto.fecha:
                initial["fechaFechaparto"] = cita_parto.fecha.strftime('%Y-%m-%d')
            initial["info_adicionalFechaparto"] = cita_parto.info_adicional 
        except ObjectDoesNotExist:
           pass

        try:
            cita_recien_nacido = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'Reciennacido')
            initial["estadoReciennacido"] = cita_recien_nacido.estado
            if cita_recien_nacido.fecha:
                initial["fechaReciennacido"] = cita_recien_nacido.fecha.strftime('%Y-%m-%d')
            initial["info_adicionalReciennacido"] = cita_recien_nacido.info_adicional
        except ObjectDoesNotExist:
            pass

        try:
            cita_puerperio = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'Puerperio')
            initial["estadoPuerperio"] = cita_puerperio.estado
            if cita_puerperio.fecha:
                initial["fechaPuerperio"] = cita_puerperio.fecha.strftime('%Y-%m-%d')
            initial["info_adicionalPuerperio"] = cita_puerperio.info_adicional 
        except ObjectDoesNotExist:
            pass

        try:
            cita_crecimiento = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'CrecimientoyDesarrollo')
            initial["estadoCrecimientoyDesarrollo"] = cita_crecimiento.estado 
            if cita_crecimiento.fecha:
                initial["fechaCrecimientoyDesarrollo"] = cita_crecimiento.fecha.strftime('%Y-%m-%d')
            initial["info_adicionalCrecimientoyDesarrollo"] = cita_crecimiento.info_adicional
        except ObjectDoesNotExist:
            pass

        try:
            cita_planificacion = Cita.objects.get(gestante_id = gestante.id, tipo_cita = 'PlanificacionFamiliar')
            initial["estadoPlanificacionFamiliar"] = cita_planificacion.estado 
            if cita_planificacion.fecha:
                initial["fechaPlanificacionFamiliar"] = cita_planificacion.fecha.strftime('%Y-%m-%d')
            initial["info_adicionalPlanificacionFamiliar"] = cita_planificacion.info_adicional
        except ObjectDoesNotExist:
            pass

        return initial


def editar_segundo_trimestre(request):
    return render(request, 'appgestantes/forms_editar/editar_segundo_trimestre.html')

def editar_tercer_trimestre(request):
    return render(request, 'appgestantes/forms_editar/editar_tercer_trimestre.html')

def editar_citas(request):
    return render(request, 'appgestantes/forms_editar/editar_citas.html')
