from django.conf.urls import url
from . import views
from django.views.generic import  DetailView, CreateView
from Programs.models import Task

urlpatterns = [
    # post views
    url(r'^$', views.home, name="home"),

    url(r'^listaTaskPGN$', views.listaTaskPGN, name='listaTaskPGN'),

    url(r'^update_task_CUST_(?P<pk>\d+)$', views.updateAttivita, name='update_task_CUST'),

    url(r'^download_(?P<pk>\d+)$', views.provaDownLoad, name='download'),

    url(r'^connection$', views.entra, name="entra"),

    url(r'^disconnection$', views.esci, name="disconnesso"),
]