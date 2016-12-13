from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^prioritarias/$', views.Prioritarias.as_view(), name='prioritarias'),
    url(r'^completa/$', views.Completa.as_view(), name='completa'),
    url(r'^pasadas/$', views.Pasadas.as_view(), name='pasadas'),
    url(r'^nueva/$', views.Nueva.as_view(), name='nueva'),
    url(r'^detalle/(?P<pk>[-\w]+)/$', views.Detalle.as_view(), name='detalle'),

    url(r'^editar_general/(?P<gestante>[-\w]+)/$', views.EditarGeneral.as_view(), name='editar_general'),
    url(r'^editar_primer_control/(?P<gestante>[-\w]+)/(?P<control>[-\w]+)/$', views.EditarPrimerControl.as_view(), name='editar_primer_control'),
    url(r'^editar_primer_trimestre/(?P<gestante>[-\w]+)/$', views.EditarPrimerTrimestre.as_view(), name='editar_primer_trimestre'),
    url(r'^editar_segundo_trimestre/(?P<gestante>[-\w]+)/$', views.EditarSegundoTrimestre.as_view(), name='editar_segundo_trimestre'),
    url(r'^editar_tercer_trimestre/(?P<gestante>[-\w]+)/$', views.EditarTercerTrimestre.as_view(), name='editar_tercer_trimestre'),
    url(r'^editar_citas/$', views.editar_citas, name='editar_citas'),
]