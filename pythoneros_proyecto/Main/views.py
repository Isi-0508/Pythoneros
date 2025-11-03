from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .pomodoro import siguiente_sesion
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import redirect

def iniciar_pomodoro(request):
    siguiente_sesion()  # 1 minuto
    return render(request, 'home.html')


@login_required(login_url='login')
def home(request):
    return render(request,"home.html")

# PENDIENTE
def about(request):
    return render(request, "about.html")

# PENDIENTE
@login_required(login_url='login')
def schedule(request):
    return HttpResponse("JOURNAL PLACEHOLDER")

def cuadrantes_view(request):
    return render(request, 'home.html')



