from django.shortcuts import render, redirect
from Programs.models import Task, Giorno, Cliente, Tecnico, Amministrativo, Utente
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil
from django import forms
from django.http import  HttpResponse, JsonResponse
import os
import MenAtWork.settings
from django.core.files import File
from django.forms import Textarea
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.

def home(request):
    inizio = 0
    return render(request, 'home.html',
                    {'inizio':inizio})

@login_required
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

            return HttpResponse('SuperuserNEW creato con successo!')
        else:
            return HttpResponse('Fallito?!?')

    else:
        form = Form_attivita()
        return render(request, 'create_task.html', {'form':form})


#------UPDATE/CREATE TASK-----------------------------------------------------------------------------------------------

class Form_TaskMF(forms.ModelForm):

    dia = forms.DateField(widget=SelectDateWidget(attrs={'class':'form-control'}),
                          initial=timezone.now())

    trabajador = forms.ModelMultipleChoiceField(queryset=Tecnico.objects.all(),
                                                required=False,
                                                widget= forms.SelectMultiple(attrs={
                                                'class':'chosen-select'
                                                }))

    class Meta:

        model = Task

        exclude = ('giorno', 'tecnici') #Questa variabile specifica i campi del model che non vanno riportati nella Form

        widgets = {'note' : Textarea(attrs={'cols': 20, 'rows': 2,
                                            'class':'form-control'}),

                   'descrizione': forms.TextInput(attrs={
                       'class':'form-control',
                       'id':'validate-text'
                   }),


                   'oraArrivo': forms.TextInput(attrs={
                       'class': 'form-control',
                       'id': 'validate-text'
                   }),

                   'cliente':forms.Select(attrs={'class':'chosen-select',}),

                    'riferimentoCommessa': forms.Select(attrs={'class': 'chosen-select', }),

                    'offerta':forms.ClearableFileInput(attrs={'class':'form-control',})

                   }

def validate_username(request):
    username = request.GET.get('username', None)


    listaFiltrata=Cliente.objects.filter(RagioneSociale__contains=username)

    results = []

    for clients in listaFiltrata:

        results.append(clients.RagioneSociale)

    return JsonResponse(results, safe=False)

@user_passes_test(lambda u: Tecnico.objects.all().filter(user_auth=u).count()>0, login_url='home')
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
            riferimentoCommessa = form.cleaned_data['riferimentoCommessa']
            note = form.cleaned_data['note']
            pianoC = form.cleaned_data['pianoCampionamento']
            ordineS = form.cleaned_data['ordineServizio']

            offerta = form.cleaned_data['offerta']

            dia = form.cleaned_data['dia']

            trabajador = form.cleaned_data['trabajador']

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
            newAttivita.riferimentoCommessa=riferimentoCommessa
            newAttivita.note=note

<<<<<<< HEAD
            if not newAttivita.pianoCampionamento:
                newAttivita.pianoCampionamento=pianoC
            if not newAttivita.ordineServizio or ordineS is False:
                newAttivita.ordineServizio=ordineS
            if not newAttivita.offerta:
=======
            if not newAttivita.pianoCampionamento or pianoC is False:
                newAttivita.pianoCampionamento=pianoC

            if not newAttivita.ordineServizio or ordineS is False:
                newAttivita.ordineServizio=ordineS

            if not newAttivita.offerta or offerta is False:
>>>>>>> parent of 759c1b9... Merge branch 'master' of https://github.com/marcelloburattini79/MenAtWork---PAG
                newAttivita.offerta=offerta

            newAttivita.tecnici.clear()

            if trabajador:
                for tecnicos in trabajador:
                    newAttivita.tecnici.add(tecnicos)



            giorno = Giorno.objects.get(giorno=dia)

            newAttivita.giorno.add(giorno)

            newAttivita.save()

            return HttpResponse('SuperuserNEW creato con successo!')
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

            form.fields['trabajador'] = forms.ModelMultipleChoiceField(queryset=Tecnico.objects.all(),
                                                                       initial=bonTrabajador,
                                                                       required=False,
                                                                        widget= forms.SelectMultiple(attrs={
                                                                        'class':'chosen-select'
                                                                        }))

            return render(request, 'create_task.html', {'form':form, 'pk':pk})



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