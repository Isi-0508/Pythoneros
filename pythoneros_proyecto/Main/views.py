from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .pomodoro import siguiente_sesion
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import redirect
from .pomodoro import disminuir_sesiones_1, aumentar_sesiones_1
from Main.pomodoro import sesiones_restantes 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
@csrf_exempt
def iniciar_pomodoro(request):
    if request.method == "POST":
        siguiente_sesion()
        return JsonResponse({"status": "ok", "mensaje": "Pomodoro iniciado"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required(login_url='login')
def aumentar_sesiones(request):
    global sesiones_restantes
    if len(sesiones_restantes) < 4:
        sesiones_restantes.append(25)
    return JsonResponse({
        "count": len(sesiones_restantes),
        "sesiones": sesiones_restantes
    })

@login_required(login_url='login')
def disminuir_sesiones(request):
    global sesiones_restantes
    if len(sesiones_restantes) > 1:
        sesiones_restantes.pop()
    return JsonResponse({
        "count": len(sesiones_restantes),
        "sesiones": sesiones_restantes
    })

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



