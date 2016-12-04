from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^prioritarias/$', views.Prioritarias.as_view(), name='prioritarias'),
    url(r'^completa/$', views.Completa.as_view(), name='completa'),
    url(r'^pasadas/$', views.Pasadas.as_view(), name='pasadas'),
    url(r'^nueva/$', views.Nueva.as_view(), name='nueva'),
    url(r'^detalle/(?P<pk>[-\w]+)/$', views.Detalle.as_view(), name='detalle'),

    url(r'^editar_general/$', views.editar_general, name='editar_general'),
    url(r'^editar_primer_control/$', views.editar_primer_control, name='editar_primer_control'),
    url(r'^editar_primer_trimestre/$', views.editar_primer_trimestre, name='editar_primer_trimestre'),
    url(r'^editar_segundo_trimestre/$', views.editar_segundo_trimestre, name='editar_segundo_trimestre'),
    url(r'^editar_tercer_trimestre/$', views.editar_tercer_trimestre, name='editar_tercer_trimestre'),
    url(r'^editar_citas/$', views.editar_citas, name='editar_citas'),
]