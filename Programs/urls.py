from django.conf.urls import url
from . import views
from django.views.generic import  DetailView, CreateView
from Programs.models import Task

urlpatterns = [
    # post views
    url(r'^$', views.home, name="home"),
    url(r'^listaTaskPGN$', views.listaTaskPGN, name='listaTaskPGN'),
    url(r'^task-detail-(?P<pk>\d+)$',DetailView.as_view(model=Task,
                                                            template_name="task_detail.html"),
                                                            name="task_detailCBV"),

    url(r'^create-taskCVB$', CreateView.as_view(model=Task,
                                                template_name="create_task.html",
                                                success_url='listaTaskPGN', fields='__all__'),
                                                name="create_taskCVB"),

    url(r'^create_task_CUST$', views.creaAttivita, name='crea_task_CUST'),

    url(r'^create_task_MF$', views.creaAttivitaMF, name='crea_task_MF'),

    url(r'^download_(?P<pk>\d+)$', views.provaDownLoad, name='download')
]