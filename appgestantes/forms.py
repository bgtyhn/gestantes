# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _

errores_defecto = {
    'required': 'Este campo se requiere',
    'invalid': 'Ingresar un dato válido'
}

class GestanteForm(forms.Form):
	nombre = forms.CharField(error_messages = errores_defecto)
	fecha_ingreso_programa = forms.DateField(error_messages = errores_defecto, required = False) #verificar
	fecha_nacimiento = forms.DateField(error_messages = errores_defecto, required = False)
	identificacion = forms.CharField(error_messages = errores_defecto, required = False)
	captacion = forms.CharField(error_messages = errores_defecto, required = False)
	semana_ingreso = forms.CharField(error_messages = errores_defecto, required = False) #verificar solo numero
	fecha_ultima_menstruacion = forms.DateField(error_messages = errores_defecto, required = False) #verificar <= hoy
	fecha_probable_parto = forms.DateField(error_messages = errores_defecto,required = False)
	confiable = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_paraclinicos = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
	pretest_fecha = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	fecha_postest = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	iami = forms.CharField(error_messages = errores_defecto, required = False)
	odontologia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	citologia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	citologia_resultado = forms.CharField(error_messages = errores_defecto, required = False)
	DPTa = forms.CharField(error_messages = errores_defecto, required = False)

class EditarGeneralForm(forms.Form):
	nombre = forms.CharField(error_messages = errores_defecto)
	fecha_probable_parto = forms.DateField(error_messages = errores_defecto, required = False)
	identificacion = forms.CharField(error_messages = errores_defecto)
	confiable = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_nacimiento = forms.DateField(error_messages = errores_defecto, required = False)
	semana_ingreso = forms.CharField(error_messages = errores_defecto, required = False) #verificar solo numero
	captacion = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_ultima_menstruacion = forms.DateField(error_messages = errores_defecto, required = False) #verificar <= hoy
	fecha_ingreso_programa = forms.DateField(error_messages = errores_defecto, required = False) #verificar
	observacion = forms.CharField(error_messages = errores_defecto, required = False)

class EditarPrimerControl(forms.Form):
	fecha_paraclinicos = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
	pretest_fecha = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	fecha_postest = forms.DateField(error_messages = errores_defecto, required = False) # > hoy
	iami = forms.CharField(error_messages = errores_defecto, required = False)
	odontologia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	citologia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	citologia_resultado = forms.CharField(error_messages = errores_defecto, required = False)
	DPTa = forms.CharField(error_messages = errores_defecto, required = False)
	texto_rie = forms.CharField(error_messages = errores_defecto, required = False)

class EditarPrimerTrimestre(forms.Form):
	cuadro_hematico = forms.CharField(error_messages = errores_defecto, required = False)
	parcial_orina = forms.CharField(error_messages = errores_defecto, required = False)
	RH = forms.CharField(error_messages = errores_defecto, required = False)
	VDRL = forms.CharField(error_messages = errores_defecto, required = False)
	VIH = forms.CharField(error_messages = errores_defecto, required = False)
	frotis_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	frotis_tipo = forms.CharField(error_messages = errores_defecto, required = False)
	factores_riesgo_diabetes_gestacional = forms.CharField(error_messages = errores_defecto, required = False)
	estado_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_factores_diabetes = forms.DateField(error_messages = errores_defecto, required = False)
	numero_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	ecografia_semanas = forms.CharField(error_messages = errores_defecto, required = False) 
	#mirar fecha parto con la ecografia
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)
	antigeno_hepatitisB = forms.CharField(error_messages = errores_defecto, required = False)
	toxoplasmosis_IGG = forms.CharField(error_messages = errores_defecto, required = False)
	toxoplasmosis_IGM = forms.CharField(error_messages = errores_defecto, required = False)
	motivo_hematico = forms.CharField(error_messages = errores_defecto, required = False)
	motivo_frotis = forms.CharField(error_messages = errores_defecto, required = False)

class EditarSegundoTrimestre(forms.Form):
	VDRL = forms.CharField(error_messages = errores_defecto, required = False)
	parcial_horina = forms.CharField(error_messages = errores_defecto, required = False)
	factores_riesgo_diabetes_gestacional = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_factores_riesgo = forms.DateField(error_messages = errores_defecto, required = False)
	estado_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	fecha_factores_diabetes = forms.DateField(error_messages = errores_defecto, required = False)
	numero_factores_diabetes = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	ecografia_semanas = forms.CharField(error_messages = errores_defecto, required = False)
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)

class EditarTercerTrimestre(forms.Form):
	VDRL = forms.CharField(error_messages = errores_defecto, required = False)
	parcial_orina = forms.CharField(error_messages = errores_defecto, required = False)
	factores_riesgo_VIH = forms.CharField(error_messages = errores_defecto, required = False) #checkbox
	fecha_VIH = forms.DateField(error_messages = errores_defecto, required = False)
	reactivo_VIH = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_unica_semanas = forms.CharField(error_messages = errores_defecto, required = False)
	ecografia_unica_fecha = forms.DateField(error_messages = errores_defecto, required = False)
	micronutrientes = forms.CharField(error_messages = errores_defecto, required = False)

class EditarCitas(forms.Form):
	estadoFechaparto = forms.CharField(error_messages = errores_defecto, required = False)
	fechaFechaparto = forms.DateField(error_messages = errores_defecto, required = False)
	info_adicionalFechaparto = forms.CharField(error_messages = errores_defecto, required = False)

	estadoReciennacido = forms.CharField(error_messages = errores_defecto, required = False)
	fechaReciennacido= forms.DateField(error_messages = errores_defecto, required = False)
	info_adicionalReciennacido = forms.CharField(error_messages = errores_defecto, required = False)

	estadoPuerperio = forms.CharField(error_messages = errores_defecto, required = False)
	fechaPuerperio = forms.DateField(error_messages = errores_defecto, required = False)
	info_adicionalPuerperio = forms.CharField(error_messages = errores_defecto, required = False)

	estadoCrecimientoyDesarrollo = forms.CharField(error_messages = errores_defecto, required = False)
	fechaCrecimientoyDesarrollo = forms.DateField(error_messages = errores_defecto, required = False)
	info_adicionalCrecimientoyDesarrollo = forms.CharField(error_messages = errores_defecto, required = False)

	estadoPlanificacionFamiliar = forms.CharField(error_messages = errores_defecto, required = False)
	fechaPlanificacionFamiliar = forms.DateField(error_messages = errores_defecto, required = False)
	info_adicionalPlanificacionFamiliar = forms.CharField(error_messages = errores_defecto, required = False)




