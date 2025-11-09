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
from .models import schedule
from django.views.decorators.clickjacking import xframe_options_exempt

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

@login_required(login_url='login')
@xframe_options_exempt
def journal(request):
    user = request.user

    #RECIBE DATOS
    if request.method == "POST":
        for key, value in request.POST.items():
            if "-" not in key:
                continue
            day, time = key.split("-")
            hour = time[:5]
            half = (time.endswith("30"))

            value = value.strip()
            if value == "":
                schedule.objects.filter(user=user, day=day, hour=hour, half=half).delete()

            else:
                schedule.objects.update_or_create(
                    user=user,
                    day=day,
                    hour=hour,
                    half=half,
                    defaults={"task_name": value}
                )
        return redirect ("journal")

    #MUESTRA EL HORARIO
    blocks = schedule.objects.filter(user=user)
    schedule_table = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    for hour in range(24):
        for half in [False, True]:
            # Se elige la hora, --:00 para false y --:30 para true
            display_time = f"{hour:02d}:00" if not half else f"{hour:02d}:30"

            # El primer elemento de la fila sera la hora
            row = {"time": display_time}

            for day in days:
                block = blocks.filter(
                    day=day,
                    hour=f"{hour:02d}:00",  # <-- FIJO ASÍ
                    half=half
                ).first()

                row[day] = block.task_name if block else ""

            schedule_table.append(row)

    return render(request, "schedule.html", {"schedule_table": schedule_table})

@login_required(login_url='login')
@xframe_options_exempt
def timer(request):
    return render(request, 'timer.html')
    
def cuadrantes_view(request):
    return render(request, 'home.html')



