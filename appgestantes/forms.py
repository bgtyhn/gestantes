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

class EditarGeneralForm(forms.Form):
	nombre = forms.CharField(error_messages = errores_defecto)
	fecha_probable_parto = forms.DateField(error_messages = errores_defecto)
	identificacion = forms.CharField(error_messages = errores_defecto)
	confiable = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_nacimiento = forms.DateField(error_messages = errores_defecto)
	semana_ingreso = forms.CharField(error_messages = errores_defecto) #verificar solo numero
	captacion = forms.CharField(error_messages = errores_defecto)
	fecha_ultima_menstruacion = forms.DateField(error_messages = errores_defecto) #verificar <= hoy
	fecha_ingreso_programa = forms.DateField(error_messages = errores_defecto) #verificar
	observacion = forms.CharField(error_messages = errores_defecto, required = False)

class EditarPrimerControl(forms.Form):
	fecha_paraclinicos = forms.DateField(error_messages = errores_defecto) # > hoy
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
	pretest_fecha = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	fecha_postest = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	iami = forms.CharField(error_messages = errores_defecto, required = False)
	odontologia_fecha = forms.DateField(error_messages = errores_defecto)
	citologia_fecha = forms.DateField(error_messages = errores_defecto)
	citologia_resultado = forms.CharField(error_messages = errores_defecto)
	DPTa = forms.CharField(error_messages = errores_defecto, required = False)
	texto_rie = forms.CharField(error_messages = errores_defecto, required = False)

class EditarPrimerTrimestre(forms.Form):
	cuadro_hematico = forms.CharField(error_messages = errores_defecto)
	parcial_orina = forms.CharField(error_messages = errores_defecto)
	RH = forms.CharField(error_messages = errores_defecto)
	VDRL = forms.CharField(error_messages = errores_defecto)
	VIH = forms.CharField(error_messages = errores_defecto)
	frotis_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	frotis_tipo = forms.CharField(error_messages = errores_defecto)
	factores_riesgo_diabetes_gestacional = forms.CharField(error_messages = errores_defecto)
	estado_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_factores_diabetes = forms.DateField(error_messages = errores_defecto, required = False)
	numero_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	ecografia_semanas = forms.CharField(error_messages = errores_defecto) 
	#mirar fecha parto con la ecografia
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
	antigeno_hepatitisB = forms.CharField(error_messages = errores_defecto)
	toxoplasmosis_IGG = forms.CharField(error_messages = errores_defecto)
	toxoplasmosis_IGM = forms.CharField(error_messages = errores_defecto)
	motivo_hematico = forms.CharField(error_messages = errores_defecto, required = False)
	motivo_frotis = forms.CharField(error_messages = errores_defecto, required = False)

class EditarSegundoTrimestre(forms.Form):
	VDRL = forms.CharField(error_messages = errores_defecto)
	parcial_horina = forms.CharField(error_messages = errores_defecto)
	factores_riesgo_diabetes_gestacional = forms.CharField(error_messages = errores_defecto)
	fecha_factores_riesgo = forms.DateField(error_messages = errores_defecto, required = False)
	estado_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_factores_diabetes = forms.DateField(error_messages = errores_defecto, required = False)
	numero_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	ecografia_semanas = forms.CharField(error_messages = errores_defecto)
	micronutrientes = forms.CharField(error_messages = errores_defecto)

class EditarTercerTrimestre(forms.Form):
	VDRL = forms.CharField(error_messages = errores_defecto, required = False)
	parcial_orina = forms.CharField(error_messages = errores_defecto, required = False)
	factores_riesgo_VIH = forms.CharField(error_messages = errores_defecto, required = False) #checkbox
	fecha_VIH = forms.DateField(error_messages = errores_defecto, required = False)
	reactivo_VIH = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_unica_semanas = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_unica_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
