from django.shortcuts import render, redirect
from Programs.models import Task, Giorno, Cliente, Tecnico, Amministrativo, Utente
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import floor
from django import forms
from django.http import  HttpResponse, JsonResponse
import os
import MenAtWork.settings
from django.core.files import File
from django.forms import Textarea
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
#Controllo GitHub

def home(request):
    inizio = 0
    return render(request, 'home.html',
                    {'inizio':inizio})

@login_required
def listaTaskPGN(request):

    listaGiorniLS = list(Giorno.objects.all())

    oggi = Giorno.objects.get(giorno=datetime.now())

    indice = listaGiorniLS.index(oggi)

    indice = floor(indice / 7)

    paginator = Paginator(listaGiorniLS, 7)

    page = request.GET.get('page')

    try:
        giorni = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        giorni = paginator.page(indice+1)

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

    offerta = forms.FileField(label = 'Offerta', required=False)

    dia = forms.DateField(widget=SelectDateWidget(), initial=timezone.now())

@user_passes_test(lambda u: u is Tecnico, login_url='home')
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

            return render(request, 'successo.html')
        else:
            return HttpResponse('Fallito?!?')

    else:
        form = Form_attivita()
        return render(request, 'create_task.html', {'form':form})


#------UPDATE/CREATE/DELETE TASK-----------------------------------------------------------------------------------------------

class Form_TaskMF(forms.ModelForm):

    dia = forms.DateField(widget=SelectDateWidget(attrs={'class':'form-control'}),
                          initial=timezone.now())

    tecnici = forms.ModelMultipleChoiceField(queryset=Tecnico.objects.all(),
                                                required=False,
                                                widget= forms.SelectMultiple(attrs={
                                                'class':'chosen-select'
                                                }))

    class Meta:

        model = Task

        exclude = ('giorno', 'tecnici', 'riferimentoCommessa') #Questa variabile specifica i campi del model che non vanno riportati nella Form

        widgets = {'note' : Textarea(attrs={'cols': 20, 'rows': 2,
                                            'class':'form-control'}),

                   'descrizione': forms.TextInput(attrs={
                       'class':'form-control',
                   }),

                   'oraArrivo': forms.TextInput(attrs={
                       'class': 'form-control',

                   }),

                   'cliente':forms.Select(attrs={'class':'chosen-select',}),


                   }

def validate_username(request):
    username = request.GET.get('username', None)


    listaFiltrata=Cliente.objects.filter(RagioneSociale__contains=username)

    results = []

    for clients in listaFiltrata:

        results.append(clients.RagioneSociale)

    return JsonResponse(results, safe=False)

@user_passes_test(lambda u:
                  u.is_authenticated and
                  u.groups.filter(name='Full').count() > 0,
                  login_url='divieto')
def updateAttivita(request, pk):
    # Questa view si occupa sia della modfica di un task che della creazione
    # Viene gestito tramite il parametro pk che viene passato
    # Se pk =='0' -> creazione altrimenti modifica

    if request.POST:
        form = Form_TaskMF(request.POST, request.FILES)

        if form.is_valid():

            descrizione = form.cleaned_data['descrizione']
            oraArrivo = form.cleaned_data['oraArrivo']
            cliente = form.cleaned_data['cliente']
            riferimentoCommessa = Amministrativo.objects.get(user_auth=request.user)
            note = form.cleaned_data['note']
            pianoC = form.cleaned_data['pianoCampionamento']
            ordineS = form.cleaned_data['ordineServizio']

            offerta = form.cleaned_data['offerta']

            dia = form.cleaned_data['dia']

            trabajador = form.cleaned_data['tecnici']

            if pk=='0':
                newAttivita = Task.objects.create(descrizione=descrizione,
                               oraArrivo=oraArrivo,
                               cliente=cliente,
                               riferimentoCommessa=riferimentoCommessa,
                               note=note,
                               offerta=offerta,
                                               )

            else:
                newAttivita = Task.objects.get(id=pk)

            newAttivita.descrizione = descrizione
            newAttivita.oraArrivo=oraArrivo
            newAttivita.cliente=cliente

            newAttivita.note=note

            if not newAttivita.ordineServizio or ordineS is False or newAttivita.ordineServizio.name == 'False':
                newAttivita.ordineServizio=ordineS

            if not newAttivita.pianoCampionamento or pianoC is False or newAttivita.pianoCampionamento.name == 'False':
                newAttivita.pianoCampionamento=pianoC

            if not newAttivita.offerta or offerta is False or newAttivita.offerta.name == 'False':
                newAttivita.offerta=offerta

            newAttivita.tecnici.clear()

            if trabajador:
                for tecnicos in trabajador:
                    newAttivita.tecnici.add(tecnicos)


            giorno = Giorno.objects.get(giorno=dia)

            newAttivita.giorno.clear() #necessario quando si modifica il giorno di un'attività

            newAttivita.giorno.add(giorno)

            newAttivita.save()

            return render(request, 'successo.html')
        else:
            return HttpResponse('Fallito?!?')

    else:

        if pk == '0':
            form = Form_TaskMF

            return render(request, 'create_task.html', {'form': form, 'pk': pk})

        else:

            attivita = Task.objects.get(id=pk)

            form = Form_TaskMF(instance=attivita)

            bomdia = form.instance.giorno.all()[0].giorno

            form.fields['dia'] = forms.DateField(widget=SelectDateWidget
            (attrs={'class':'form-control'}), initial=bomdia)


            bonTrabajador = form.instance.tecnici.all()

            form.fields['tecnici'] = forms.ModelMultipleChoiceField(queryset=Tecnico.objects.all(),
                                                                       initial=bonTrabajador,
                                                                       required=False,
                                                                        widget= forms.SelectMultiple(attrs={
                                                                        'class':'chosen-select'
                                                                        }))

            return render(request, 'create_task.html', {'form':form, 'pk':pk})

def divieto(request):
    return render(request, 'divietoAcc.html')

def deleteTask(request, pk):

    if request.POST:

        attivitaDel = Task.objects.get(id=pk)

        attivitaDel.delete()

        return render (request, 'successo.html')


#-------UPDATE GIORNO---------------------------------------------------------------------------------------------------

class Form_Giorno(forms.ModelForm):

    personale_assente = forms.ModelMultipleChoiceField(queryset=Tecnico.objects.all(),
                                             required=False,
                                             widget=forms.SelectMultiple(attrs={
                                                 'class': 'chosen-select'
                                             }))

    class Meta:

        model = Giorno

        exclude = ('giorno', 'personaleAssente',)


@user_passes_test(lambda u:
                  u.is_authenticated and
                  u.groups.filter(name='Full').count() > 0,
                  login_url='divieto')
def updateGiorno(request, pk):
    if request.POST:
        form = Form_Giorno(request.POST)

        if form.is_valid():

            trabajador = form.cleaned_data['personale_assente']

            dia = Giorno.objects.get(id=pk)

            dia.personaleAssente.clear()

            if trabajador:
                for tecnicos in trabajador:
                    dia.personaleAssente.add(tecnicos)

            dia.save()

            return render(request, 'successo.html')

        else:
            return HttpResponse('Fallito?!?')

    else:

        dia = Giorno.objects.get(id=pk)

        form = Form_Giorno(instance=dia)

        bonTrabajador = form.instance.personaleAssente.all()

        form.fields['personale_assente'] = forms.ModelMultipleChoiceField(queryset=Tecnico.objects.all(),
                                                                initial=bonTrabajador,
                                                                required=False,
                                                                widget=forms.SelectMultiple(attrs={
                                                                    'class': 'chosen-select'
                                                                }))

        return render(request, 'updateGiorno.html', {'form': form, 'pk': pk, 'dia':dia})


#-------LOGIN/LOGOUT----------------------------------------------------------------------------------------------------

class Form_connection(forms.Form):

    username = forms.CharField(label="Login",
                               widget = forms.TextInput(
                                   attrs={
                                       'class':'form-control',
                                       'id' : 'inputEmail',
                                       'placeholder':'Username',
                                       'required': 'True',
                                       'autofocus':'True'
                                   }
                               ))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(
                                attrs={
                                    'class': 'form-control',
                                    'id' : "inputPassword",
                                    'required' : 'True',
                                    'placeholder' : 'Password'
                                }
                               ))

    def clean(self):
        cleaned_data = super(Form_connection, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")

        return self.cleaned_data

def entra(request):

    if request.POST:
        form = Form_connection(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                if request.GET.get('next') is not None:
                    return redirect(request.GET['next'])

                else:
                    return render(request, 'connection.html', {'form': form,
                                                           'user': user})

            else:
                return render(request, 'connection.html', {'form': form,
                                                           'user':user})

        else:
            return render(request, 'connection.html', {'form': form})

    else:
        form = Form_connection()
        return render(request, 'connection.html', {'form': form})

def esci(request):
    logout(request)
    return render(request, 'home.html')

class Form_changePass(forms.Form):


    nuova_password = forms.CharField(label="Nuova Password",
                               widget=forms.PasswordInput(
                                attrs={
                                    'class': 'form-control',
                                    'id' : "inputPassword",
                                    'required' : 'True',
                                    'placeholder' : 'Password'
                                }
                               ))

    ripeti_password = forms.CharField(label="Ripeti Password",
                                     widget=forms.PasswordInput(
                                         attrs={
                                             'class': 'form-control',
                                             'id': "inputPassword",
                                             'required': 'True',
                                             'placeholder': 'Password'
                                         }
                                     ))


    def clean(self):
        cleaned_data = super(Form_changePass, self).clean()

        nuova_password = self.cleaned_data.get('nuova_password')
        ripeti_password = self.cleaned_data.get('ripeti_password')

        if nuova_password != ripeti_password:
            raise forms.ValidationError("Le password non coincidono. Riprova")

        return self.cleaned_data

def changePass(request):

    if request.POST:

        form = Form_changePass(request.POST)

        if form.is_valid():

            request.user.set_password(form.cleaned_data["nuova_password"])

            request.user.save()

            login(request, request.user)

            return render(request, 'successo.html')

        else:
            return render(request, 'noChange.html')

    else:
        form = Form_changePass()
        return render(request, 'changePass.html', {'form': form})



#---------METODI X IL DOWNLOAD----------------------------------------------------------------------------------------------------------

def provaDownLoad(request, pk):

    attivita = Task.objects.get(id=pk)

    path_to_file = (os.path.join(MenAtWork.settings.BASE_DIR, '', attivita.offerta.name))
    f = open(path_to_file, 'rb')
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + attivita.offerta.name

    myfile.close()

    f.close()

    return response

def pianoDL(request, pk):

    attivita = Task.objects.get(id=pk)

    path_to_file = (os.path.join(MenAtWork.settings.BASE_DIR, '', attivita.pianoCampionamento.name))
    f = open(path_to_file, 'rb')
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + attivita.pianoCampionamento.name

    myfile.close()

    f.close()

    return response

def ordineDL(request, pk):

    attivita = Task.objects.get(id=pk)

    path_to_file = (os.path.join(MenAtWork.settings.BASE_DIR, '', attivita.ordineServizio.name))
    f = open(path_to_file, 'rb')
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + attivita.ordineServizio.name

    myfile.close()

    f.close()

    return response