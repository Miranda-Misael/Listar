#from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError # controlas los errrores de integridad con la DB
from django.contrib.auth import login, logout, authenticate
#from tasks.forms import TaskForm
#from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def helloworlduser (request):
    return HttpResponse('Hello World Usuarios')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm
                                               })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('menu')
            except IntegrityError: # controla los errores de integridad en la DB
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': '- Usuario ya existe -'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseñas no coinciden'
        })
    
@login_required #Valida que un usuario para acceder deba estar logueado
def signout(request):
    logout(request)
    return redirect('home')    


def signin(request):  # recibe una peticion
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        # print(request.POST)
        user = authenticate(  # me va a devolver un usuario
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('menu')