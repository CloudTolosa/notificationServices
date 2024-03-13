from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django import forms
from  .models import *
from .scrapping import generar_web_scrapping
from django_cron import CronJobBase, Schedule
import pandas as pd
from twilio.rest import Client
from datetime import date, timedelta
from django.http import HttpResponse
#from django_crontab import daily

# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile  # Establece el modelo de usuario en User
        fields = ('username', 'barrio')  # Los campos que se mostrarán en el formulario
        widgets = {
            'barrio': forms.Select(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False  # Hacer que los campos de contraseña no sean obligatorios
        self.fields['password2'].required = False

def home_list(request):
    contex = {
        'form': CustomUserCreationForm()
    }
    if request.method=='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(request, 'servicios/home_list.html',contex)



def send_message(request):
    print(request)
    fecha_actual = date.today()
    fecha_siguiente = fecha_actual + timedelta(days=1)
    account_sid = 'ACe57c7d027de7cc623d367042f681be03'
    auth_token = '4ed73b4f420d6507765356c1ebd39ed2'
    body = f"Te avisamos que en el barrio {request.barrio.nombre} tendrá previstos cortes de agua el día {fecha_siguiente.strftime('%A, %d de %B de %Y')}, te recomendamos tener provisiones de agua en tu hogar 😊 🚱🤽‍♂️🚱"
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+13017100811',
                        to='+57'+str(request.username)
                    )

    print(message.sid)

class Scrapping(CronJobBase):
    def do(self):
        account_sid = 'ACe57c7d027de7cc623d367042f681be03'
        auth_token = '4ed73b4f420d6507765356c1ebd39ed2'
        client = Client(account_sid, auth_token)
        barrios_web_scrapping = generar_web_scrapping()
        df = pd.DataFrame(barrios_web_scrapping)
        df=df['Barrios'].str.split(', ')
        barrios_list=df.tolist()[0]
        barrios_list = [elemento.rstrip('.') for elemento in barrios_list]
        print(barrios_list)
        usuarios= UserProfile.objects.filter(barrio__nombre__in=barrios_list)
        for usuario in usuarios:
            send_message(usuario)

def sent_message(request):
    barrios_web_scrapping = generar_web_scrapping()
    df = pd.DataFrame(barrios_web_scrapping)
    df=df['Barrios'].str.split(', ')
    barrios_list=df.tolist()[0]
    barrios_list = [elemento.rstrip('.') for elemento in barrios_list]
    
    usuarios= UserProfile.objects.filter(barrio__nombre__in=barrios_list)
    for usuario in usuarios:
        send_message(usuario)
    
    return HttpResponse("Message sent successfully")