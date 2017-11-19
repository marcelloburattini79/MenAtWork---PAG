from django.contrib import admin

from Programs.models import Tecnico, Amministrativo, Cliente, Task, Giorno



# Register your models here.

admin.site.register(Tecnico)

admin.site.register(Amministrativo)

admin.site.register(Cliente)

admin.site.register(Task)

admin.site.register(Giorno)