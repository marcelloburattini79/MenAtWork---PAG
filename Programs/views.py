from django.shortcuts import render
from Programs.models import Task, Giorno, Cliente, Tecnico, Amministrativo
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect
import os
import MenAtWork.settings
from django.core.files import File
from django.forms import Textarea
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone




# Create your views here.

def home(request):
    inizio = 0
    return render(request, 'home.html',
                    {'inizio':inizio})

def listaTaskPGN(request):

    listaGiorniLS = list(Giorno.objects.all())

    oggi = Giorno.objects.get(giorno=datetime.now())

    indice = listaGiorniLS.index(oggi)

    indice = ceil(indice / 7)

    paginator = Paginator(listaGiorniLS, 7)

    page = request.GET.get('page')

    try:
        giorni = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        giorni = paginator.page(indice)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        giorni = paginator.page(paginator.num_pages)

    return render(request, 'listaTaskPGN.html', {'giorni': giorni})

class Form_attivita(forms.Form):

    descrizione = forms.CharField(label="Descrizione", max_length=200)

    oraArrivo = forms.CharField(max_length=500, label='Ora di arrivo')

    cliente = forms.ModelChoiceField(label="Cliente", queryset=Cliente.objects.all().order_by('RagioneSociale'))

    tecnici = forms.ModelMultipleChoiceField(label='Tecnici',
                                             queryset=Tecnico.objects.all())


    riferimentoCommessa = forms.ModelChoiceField(label="Commessa",
                            queryset=Amministrativo.objects.all())


    note = forms.CharField(label='Note', widget=forms.Textarea, required=False)

    offerta = forms.FileField(label = 'Offerta')

    #giorno = forms.ModelMultipleChoiceField(label='Data',queryset = Giorno.objects.order_by('giorno'))

    dia = forms.DateField(widget=SelectDateWidget(), initial=timezone.now())


def creaAttivita(request):
    if request.POST:
        form = Form_attivita(request.POST, request.FILES)

        if form.is_valid():

            descrizione = form.cleaned_data['descrizione']
            oraArrivo = form.cleaned_data['oraArrivo']
            cliente = form.cleaned_data['cliente']
            tecnici = form.cleaned_data['tecnici']
            riferimentoCommessa = form.cleaned_data['riferimentoCommessa']
            note = form.cleaned_data['note']

            offerta = form.cleaned_data['offerta']

            dia = form.cleaned_data['dia']

            newAttivita = Task.objects.create(descrizione=descrizione,
                               oraArrivo=oraArrivo,
                               cliente=cliente,
                               riferimentoCommessa=riferimentoCommessa,
                               note=note,
                               offerta=offerta,
                                               )
            for tecnicos in tecnici:
                newAttivita.tecnici.add(tecnicos)


            giorno = Giorno.objects.get(giorno=dia)

            newAttivita.giorno.add(giorno)

            newAttivita.save()

            return HttpResponse('SuperuserNEW creato con successo!')
        else:
            return HttpResponse('Fallito?!?')

    else:
        form = Form_attivita()
        return render(request, 'create_task.html', {'form':form})

def taskDettagli(request, pk):

    attivitaCheck = Task.objects.filter(id = pk)

    attivita = attivitaCheck.get()

def provaDownLoad(request, pk):
    '''
    fh = open(os.path.join(MenAtWork.settings.BASE_DIR, 'offerte\\27.10.1713.pdf'), 'r')

    response = HttpResponse(fh.read(), content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=27.10.1713.pdf'
    return response
    '''

    attivita = Task.objects.get(id=pk)

    path_to_file = (os.path.join(MenAtWork.settings.BASE_DIR, '', attivita.offerta.name))
    f = open(path_to_file, 'rb')
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + attivita.offerta.name

    myfile.close()

    f.close()

    return response


class Form_TaskMF(forms.ModelForm):
    #from_date = forms.DateField(widget=AdminDateWidget())

    dia = forms.DateField(widget=SelectDateWidget(), initial=timezone.now())

    class Meta:

        model = Task

        exclude = ('giorno',) #Questa variabile specifica i campi del model che vanno riportati nella Form

        widgets = {'note' : Textarea(attrs={'cols': 20, 'rows': 8}),}




def creaAttivitaMF(request):

    if len(request.POST)> 0:

        form = Form_TaskMF(request.POST, request.FILES)

        if form.is_valid:

            form.save(commit=True)

            form.giorno = form.cleaned_data['dia']

            form.save()

            return HttpResponseRedirect('listaTaskPGN')

        else:
            return HttpResponse('Form non vallido')

    else:
        form = Form_TaskMF()

        return render(request, 'create_taskMF.html', {'form':form})
