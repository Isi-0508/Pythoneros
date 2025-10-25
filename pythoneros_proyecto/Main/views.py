from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .pomodoro import temporizador_pomodoro

def iniciar_pomodoro(request):
    temporizador_pomodoro(5)  # 5 minuto
    return HttpResponse("Pomodoro iniciado en segundo plano.")


# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,"home.html")
