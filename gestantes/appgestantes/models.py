# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

CAPTACION = (
	('Médico','Médico'),
	('Enfermera','Enfermera'),
	('Atención primaria en salud', 'Atención primaria en salud')
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
	('En tratamiento', 'En tratamiento')
)

VDRL = (
	('Reactivo', 'Reactivo'),
	('No reactivo', 'No reactivo')
)

VIH = (
	('Reactivo', 'Reactivo'),
	('No reactivo', 'No reactivo')
)

FROTIS = (
	('Normal', 'Normal'),
	('Alterado', 'Alterado')
)

ANTIGENO = (
	('Reactivo', 'Reactivo'),
	('No reactivo', 'No reactivo'),
	('Pendiente', 'Pendiente'),
)

TOXOPLASMOSIS_IGG = (
	('IGG Positiva', 'IGG Positiva'),
	('IGG Negativa', 'IGG Negativa'),
)

TOXOPLASMOSIS_IGM = (
	('IGM Positiva', 'IGG Positiva'),
	('IGM Negativa', 'IGG Negativa'),
)

TIPO_CITA = (
	('Fecha parto', 'Fecha parto'),
	('Recien nacido', 'Recien nacido'),
	('Puerperio', 'Puerperio'),
	('Crecimiento y Desarrollo', 'Crecimiento y Desarrollo'),
	('Planificación Familiar', 'Planificación Familiar')
)

ESTADO_CITA = (
	('Pendiente', 'Pendiente'),
	('Atendida', 'Atendida'),
)

class Gestante(models.Model):
	nombre = models.CharField(max_length=100)
	fecha_ingreso_programa = models.DateField() #verificar
	fecha_nacimiento = models.DateField()
	identificacion = models.CharField(max_length = 15)
	captacion = models.CharField(max_length = 40, choices = CAPTACION)
	semana_ingreso = models.CharField(max_length = 10) #verificar solo numero
	fecha_ultima_menstruacion = models.DateField() #verificar <= hoy
	fecha_probable_parto = models.DateField()
	confiable = models.CharField(max_length = 20)

class PrimerControl(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	fecha_paraclinicos = models.DateField() # > hoy
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES)
	pretest_fecha = models.DateField() # > hoy
	fecha_postest = models.DateField() # > hoy
	iami = models.CharField(max_length = 3, choices = SI_OPCIONES)
	odontologia_fecha = models.DateField()
	citologia_fecha = models.DateField()
	citologia_resultado = models.TextField()
	DPTa = models.CharField(max_length = 3, choices = SI_OPCIONES)

class Riesgo(models.Model):
	primerControl = models.ForeignKey(PrimerControl, on_delete = models.CASCADE)
	motivo = models.TextField()

class PrimerTrimestre(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	cuadro_hematico = models.CharField(max_length = 10, choices = CUADRO_HEMATICO) #hacer otra tabla lista
	parcial_orina = models.CharField(max_length = 40, choices = PARCIAL_ORINA)
	RH = models.TextField()
	VDRL = models.CharField(max_length = 20, choices = VDRL)
	VIH = models.CharField(max_length = 20, choices = VIH)
	frotis_fecha = models.DateField()
	frotis_tipo = models.CharField(max_length = 15, choices = FROTIS) #hacer otra tabla lista
	factores_riesgo_diabetes_gestacional = models.CharField(max_length = 3, choices = SI_OPCIONES) # otra tabla con un numero
	ecografia_fecha = models.DateField()
	ecografia_semanas = models.CharField(max_length = 5) #verificar solo numero
	#mirar fecha parto con la ecografia
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES)
	antigeno_hepatitisB = models.CharField(max_length = 15, choices = ANTIGENO)
	toxoplasmosis_IGG = models.CharField(max_length = 20, choices = TOXOPLASMOSIS_IGG)
	toxoplasmosis_IGM = models.CharField(max_length = 20, choices = TOXOPLASMOSIS_IGM)

class SegundoTrimestre(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	VDRL = models.CharField(max_length = 20, choices = VDRL)
	parcial_horina = models.CharField(max_length = 40, choices = PARCIAL_ORINA) #otra tabla
	ecografia_fecha = models.DateField()
	ecografia_semanas = models.CharField(max_length = 5) #verificar solo numero
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES)

class TercerTrimestre(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	VDRL = models.CharField(max_length = 20, choices = VDRL)
	parcial_orina = models.CharField(max_length = 40, choices = PARCIAL_ORINA)
	factores_riesgo_VIH = models.CharField(max_length = 3, choices = SI_OPCIONES)
	ecografia_unica_semanas = models.CharField(max_length = 5) #verificar numero
	ecografia_unica_fecha = models.DateField()
	micronutrientes = models.CharField(max_length = 3, choices = SI_OPCIONES)

class Cita(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	tipo_cita = models.CharField(max_length = 40, choices = TIPO_CITA)
	estado = models.CharField(max_length = 15, choices = ESTADO_CITA)
	fecha = models.DateField()
	info_adicional = models.TextField()

class Observacion(models.Model):
	gestante = models.ForeignKey(Gestante, on_delete = models.CASCADE)
	texto = models.TextField()
