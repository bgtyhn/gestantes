from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prioritarias/$', views.prioritarias, name='prioritarias'),
    url(r'^completa/$', views.completa, name='completa'),
    url(r'^pasadas/$', views.pasadas, name='pasadas'),
    url(r'^nueva/$', views.nueva, name='nueva'),
    url(r'^detalle/$', views.detalle, name='detalle')
]