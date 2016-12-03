from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^prioritarias/$', views.Prioritarias.as_view(), name='prioritarias'),
    url(r'^completa/$', views.Completa.as_view(), name='completa'),
    url(r'^pasadas/$', views.Pasadas.as_view(), name='pasadas'),
    url(r'^nueva/$', views.Nueva.as_view(), name='nueva'),
    url(r'^detalle/(?P<pk>[-\w]+)/$', views.Detalle.as_view(), name='detalle')
]