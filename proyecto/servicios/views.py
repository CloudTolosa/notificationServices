from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django import forms
from  .models import *
import ssl
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
            username = form.cleaned_data['username']  # Obtener el nombre de usuario del formulario
            #form.save()
            send_message_welcome(username)  # Pasar el nombre de usuario a la función send_message_welcome
        else:
            print(form.errors)
    return render(request, 'servicios/home_list.html',contex)



def send_message(request):
    print(request)
    fecha_actual = date.today()
    fecha_siguiente = fecha_actual + timedelta(days=1)
    account_sid = 'ACe57c7d027de7cc623d367042f681be03'
    auth_token = '733c9ceab7d9dc4b46eb20014f56f8cf'
    body = f"Te avisamos que en el barrio {request.barrio.nombre} tendrá previstos cortes de agua el día {fecha_siguiente.strftime('%A, %d de %B de %Y')}, te recomendamos tener provisiones de agua en tu hogar 😊 🚱🤽‍♂️🚱"
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+13017100811',
                        to='+57'+str(request.username)
                    )

    print(message.sid)

def send_message_welcome(request):
    #ssl._create_default_https_context = ssl._create_unverified_context
    print('usuario')
    print(request)
    account_sid = 'ACe57c7d027de7cc623d367042f681be03'
    #US0f5c1f8a2415f76ea83b8d95c17669be
    auth_token = '733c9ceab7d9dc4b46eb20014f56f8cf'
    body = 'Te damos la bienvenida a Noti Ciudad Bolivar te avisaremos de los cortes previstos de agua con un dia de anticipacion 😊 🚱🤽‍♂️🚱'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+13017100811',
                        to='+57'+str(request)
                    )

    print(message.sid)
