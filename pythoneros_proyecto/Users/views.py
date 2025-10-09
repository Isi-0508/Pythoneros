from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

#(!) CORREGIR

#LOGIN/REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2]'] #Confirmar contraseña

        #Exigencias de contraseña (Quizas hacerla mas segura, min 8 caracteres, maximo 15)
        #Verificación
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Este usuario ya existe, intentelo de nuevo")
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Bienvenido a FOCUSTOM")
                return redirect('login')
        else:
            messages.error(request, "Las contraseñas no coinciden")

    return render(request, "register_page.html")

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    attempts = 0 #Quiero poner algo para ayudar al usuario a hacer un olvidar contraseña

    flag1 = False
    flag2 = False
    usernamewrong = "Usuario Incorrecto"
    passwordwrong = "Contraseña Incorrecta"

    #Primero revisa las 2 cosas antes de informar un error
    if User.objects.filter(username=username).exists():
        flag1 = True
    else:
        flag1 = False

    if User.objects.filter(password=password).exists():
        flag2 = True
    else:
        flag2 = False

    if flag1 and not flag2:
        messages.error(request, "(!) Usuario Incorrecto, intentelo de nuevo")
    if not flag1 and flag2:
        messages.error(request, "(!) Contraseña Incorrecta, intentelo de nuevo")
    if not flag1 and not flag2:
        messages.error(request, "(!) Usuario y Contraseña incorrectos, intentelo de nuevo")

    return render(request,"login_page.html")
