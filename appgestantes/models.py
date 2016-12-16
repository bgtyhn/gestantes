# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator

CAPTACION = (
	('Médico','Médico'),
	('Enfermera','Enfermera'),
	('Atención', 'Atención primaria en salud')
)

SI_OPCIONES = (
	('Si', 'Si'),
	('No', 'No'),
)

RIESGO = (
	('Alto', 'Alto'),
	('Bajo', 'Bajo'),
)

CUADRO_HEMATICO = (
	('Normal', 'Normal'),
	('Anormal', 'Anormal'),
)

PARCIAL_ORINA = (
	('Normal', 'Normal'),
	('Tratamiento', 'En tratamiento')
)

VDRL = (
	('Reactivo', 'Reactivo'),
	('NoReactivo', 'No reactivo')
)

VIH = (
	('Pendiente', 'Pendiente'),
	('Reactivo', 'Reactivo'),
	('NoReactivo', 'No reactivo')
)

FROTIS = (
	('Pendiente', 'Pendiente'),
	('Normal', 'Normal'),
	('Alterado', 'Alterado')
)

ANTIGENO = (
	('Reactivo', 'Reactivo'),
	('NoReactivo', 'No reactivo'),
	('Pendiente', 'Pendiente'),
)

TOXOPLASMOSIS_IGG = (
	('IGGPositiva', 'IGG Positiva'),
	('IGGNegativa', 'IGG Negativa'),
)

TOXOPLASMOSIS_IGM = (
	('IGMPositiva', 'IGM Positiva'),
	('IGMNegativa', 'IGM Negativa'),
)

TIPO_CITA = (
	('Fechaparto', 'Fecha parto'),
	('Reciennacido', 'Recien nacido'),
	('Puerperio', 'Puerperio'),
	('CrecimientoyDesarrollo', 'Crecimiento y Desarrollo'),
	('PlanificacionFamiliar', 'Planificación Familiar')
)

ESTADO_CITA = (
	('Ninguno', 'Ninguno'),
	('Pendiente', 'Pendiente'),
	('Atendida', 'Atendida'),
)

NUMERIC = RegexValidator(r'^[0-9]*$', 'Solo se permiten números')

class Gestante(models.Model):
	nombre = models.CharField(max_length=100)
	fecha_ingreso_programa = models.DateField() #verificar
	edad = models.CharField(max_length = 3, validators=[NUMERIC], null=True, blank=True)
	identificacion = models.CharField(max_length = 15, null=True, blank=True)
	captacion = models.CharField(max_length = 40, choices = CAPTACION)
	semana_ingreso = models.CharField(max_length = 10, validators=[NUMERIC]) #verificar solo numero
	fecha_ultima_menstruacion = models.DateField(null=True, blank=True) #verificar <= hoy
	fecha_probable_parto = models.DateField(null=True, blank=True)
	confiable = models.CharField(max_length = 20, default = 'No')
	EPS = models.CharField(max_length = 40, null = True, blank = True)

class PrimerControl(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	fecha_paraclinicos = models.DateField(blank=True, null=True) # > hoy
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES)
	pretest_fecha = models.DateField(blank=True, null=True) # > hoy
	fecha_postest = models.DateField(blank=True, null=True) # > hoy
	iami = models.CharField(max_length = 3, default = 'No' ,choices = SI_OPCIONES)
	odontologia_fecha = models.DateField(blank=True, null=True)
	citologia_fecha = models.DateField(blank=True, null=True)
	citologia_resultado = models.TextField(null=True, blank=True)
	DPTa = models.CharField(max_length = 3, default = 'No' , choices = SI_OPCIONES)

class Riesgo(models.Model):
	primerControl = models.ForeignKey(PrimerControl, on_delete = models.CASCADE)
	motivo = models.TextField()

class PrimerTrimestre(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	cuadro_hematico = models.CharField(max_length = 10, choices = CUADRO_HEMATICO)
	parcial_orina = models.CharField(max_length = 40, choices = PARCIAL_ORINA)
	RH = models.TextField(null=True, blank=True)
	VDRL = models.CharField(max_length = 20, choices = VDRL, null=True, blank=True)
	VIH = models.CharField(max_length = 20, choices = VIH, null=True, blank=True)
	frotis_fecha = models.DateField(blank=True, null=True)
	frotis_tipo = models.CharField(max_length = 15, choices = FROTIS, null=True, blank=True)
	factores_riesgo_diabetes_gestacional = models.CharField(max_length = 3, choices = SI_OPCIONES, null=True, blank=True)
	estado_factores_diabetes = models.CharField(max_length = 15, choices = FROTIS, blank=True, null=True)
	fecha_factores_diabetes = models.DateField(blank=True, null=True)
	numero_factores_diabetes = models.CharField(max_length = 5, validators=[NUMERIC], blank=True, null=True) 
	ecografia_fecha = models.DateField(blank=True, null=True)
	ecografia_semanas = models.CharField(max_length = 5, validators=[NUMERIC], null=True, blank=True) 
	#mirar fecha parto con la ecografia
	micronutrientes = models.CharField(max_length = 3, default = 'No' ,choices = SI_OPCIONES, null=True, blank=True)
	antigeno_hepatitisB = models.CharField(max_length = 15, choices = ANTIGENO, null=True, blank=True)
	toxoplasmosis_IGG = models.CharField(max_length = 20, choices = TOXOPLASMOSIS_IGG, null=True, blank=True)
	toxoplasmosis_IGM = models.CharField(max_length = 20, choices = TOXOPLASMOSIS_IGM, null=True, blank=True)

class ListaMotivosCHPT(models.Model):
	primer_trimestre = models.ForeignKey(PrimerTrimestre, on_delete = models.CASCADE)
	motivo = models.TextField(null=True, blank=True)

class ListaMotivosFrotisPT(models.Model):
	primer_trimestre = models.ForeignKey(PrimerTrimestre, on_delete = models.CASCADE)
	motivo = models.TextField(null=True, blank=True)

class SegundoTrimestre(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	VDRL = models.CharField(max_length = 20, choices = VDRL,null=True, blank=True)
	parcial_horina = models.CharField(max_length = 40, choices = PARCIAL_ORINA, null=True, blank=True)
	factores_riesgo_diabetes_gestacional = models.CharField(max_length = 3, choices = SI_OPCIONES, null=True, blank=True)
	fecha_factores_riesgo = models.DateField(blank=True, null=True)
	estado_factores_diabetes = models.CharField(max_length = 15, choices = FROTIS, blank=True, null=True)
	fecha_factores_diabetes = models.DateField(blank=True, null=True)
	numero_factores_diabetes = models.CharField(max_length = 5, validators=[NUMERIC], blank=True, null=True)
	ecografia_fecha = models.DateField(blank=True, null=True)
	ecografia_semanas = models.CharField(max_length = 5, validators=[NUMERIC], null=True, blank=True) 
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES, null=True, blank=True)

class TercerTrimestre(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	VDRL = models.CharField(max_length = 20, choices = VDRL, null=True, blank=True)
	parcial_orina = models.CharField(max_length = 40, choices = PARCIAL_ORINA, null=True, blank=True)
	factores_riesgo_VIH = models.CharField(max_length = 3, choices = SI_OPCIONES, null=True, blank=True)
	fecha_VIH = models.DateField(blank=True, null=True)
	reactivo_VIH = models.CharField(max_length = 40, choices = VIH, null=True, blank=True)
	ecografia_unica_semanas = models.CharField(max_length = 5, validators=[NUMERIC], null=True, blank=True) 
	ecografia_unica_fecha = models.DateField(blank=True, null=True)
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES, null=True, blank=True)

class Cita(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	tipo_cita = models.CharField(max_length = 40, choices = TIPO_CITA, null=True, blank=True)
	estado = models.CharField(max_length = 15, choices = ESTADO_CITA, null=True, blank=True)
	fecha = models.DateField(blank=True, null=True)
	info_adicional = models.TextField(null=True, blank=True)

class Observacion(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	texto = models.TextField(null=True, blank=True)
