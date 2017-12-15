from django.conf.urls import url
from . import views
from django.views.generic import  DetailView, CreateView
from Programs.models import Task

urlpatterns = [
    # post views
    url(r'^$', views.home, name="home"),

    url(r'^divieto$', views.divieto, name="divieto"),

    url(r'^listaTaskPGN$', views.listaTaskPGN, name='listaTaskPGN'),

    url(r'^update_task_CUST_(?P<pk>\d+)$', views.updateAttivita, name='update_task_CUST'),

    url(r'^delete_task_(?P<pk>\d+)$', views.deleteTask, name='delete_task'),

    url(r'^update_giorno_(?P<pk>\d+)$', views.updateGiorno, name='update_giorno'),

    url(r'^download_(?P<pk>\d+)$', views.provaDownLoad, name='download'),

    url(r'^pianoDL_(?P<pk>\d+)$', views.pianoDL, name='pianoDL'),

    url(r'^ordineDL_(?P<pk>\d+)$', views.ordineDL, name='ordineDL'),

    url(r'^connection$', views.entra, name="entra"),

    url(r'^changePass$', views.changePass, name="changePass"),

    url(r'^disconnection$', views.esci, name="disconnesso"),

    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),

]