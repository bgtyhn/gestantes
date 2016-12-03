# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _

errores_defecto = {
    'required': 'Este campo se requiere',
    'invalid': 'Ingresar un dato válido'
}

class ModelGestanteForm(forms.ModelForm):
	class Meta:
		model = Gestante
		fields = ('nombre', 'fecha_ingreso_programa', 'fecha_nacimiento', 'identificacion', 'captacion', 'semana_ingreso', 'fecha_ultima_menstruacion', 'fecha_probable_parto', 'confiable')
		error_messages = {
			'nombre':{
				'required' : _('Por favor llene el campo')
			},
			'fecha_ingreso_programa':{
				'required' : _('Por favor llene el campo')
			},
			'fecha_nacimiento':{
				'required' : _('Por favor seleccione una imagen'),
				'invalid' : _('Por favor seleccione un archivo de imagen')
			},
			'identificacion':{
				'required' : _('Por favor llene el campo')
			},
			'captacion':{
				'required' : _('Por favor llene el campo')
			},
			'semana_ingreso':{
				'required' : _('Por favor llene el campo')
			},
			'fecha_ultima_menstruacion':{
				'required' : _('Por favor llene el campo')
			},
			'fecha_probable_parto':{
				'required' : _('Por favor llene el campo')
			},
			'confiable':{
				'required' : _('Por favor llene el campo')
			},

		}

class ModelPrimerControlForm(forms.ModelForm):
	class Meta:
		model = PrimerControl
		fields = ('fecha_paraclinicos', 'micronutrientes', 'pretest_fecha', 'fecha_postest', 'iami', 'odontologia_fecha', 'citologia_fecha', 'citologia_resultado', 'DPTa')
		error_messages = {
			'fecha_paraclinicos':{
				'required' : _('Por favor llene el campo')
			},
			'micronutrientes':{
				'required' : _('Por favor seleccione una imagen'),
				'invalid' : _('Por favor seleccione un archivo de imagen')
			},
			'pretest_fecha':{
				'required' : _('Por favor llene el campo')
			},
			'fecha_postest':{
				'required' : _('Por favor llene el campo')
			},
			'iami':{
				'required' : _('Por favor llene el campo')
			},
			'odontologia_fecha':{
				'required' : _('Por favor llene el campo')
			},
			'citologia_fecha':{
				'required' : _('Por favor llene el campo')
			},
			'citologia_resultado':{
				'required' : _('Por favor llene el campo')
			},
			'DPTa':{
				'required' : _('Por favor llene el campo')
			},
		}


class GestanteForm(forms.Form):
	nombre = forms.CharField(error_messages = errores_defecto)
	fecha_ingreso_programa = forms.DateField(error_messages = errores_defecto) #verificar
	fecha_nacimiento = forms.DateField(error_messages = errores_defecto)
	identificacion = forms.CharField(error_messages = errores_defecto)
	captacion = forms.CharField(error_messages = errores_defecto)
	semana_ingreso = forms.CharField(error_messages = errores_defecto) #verificar solo numero
	fecha_ultima_menstruacion = forms.DateField(error_messages = errores_defecto) #verificar <= hoy
	fecha_probable_parto = forms.DateField(error_messages = errores_defecto)
	confiable = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_paraclinicos = forms.DateField(error_messages = errores_defecto) # > hoy
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
	pretest_fecha = forms.DateField(error_messages = errores_defecto) # > hoy
	fecha_postest = forms.DateField(error_messages = errores_defecto) # > hoy
	iami = forms.CharField(error_messages = errores_defecto, required = False)
	odontologia_fecha = forms.DateField(error_messages = errores_defecto)
	citologia_fecha = forms.DateField(error_messages = errores_defecto)
	citologia_resultado = forms.CharField(error_messages = errores_defecto)
	DPTa = forms.CharField(error_messages = errores_defecto, required = False)