from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.

#(!) CORREGIR
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
strangechar = "!@#$%^&*()-_=+[];:,.<>/?"

#La contraseña debe contener al menos:
#-8 caracteres, de ellos:
# 4 letras, 2 numeros y 2 caracteres raros
#LOGIN/REGISTER

def passwordcheck(password):
    letters_count = 0
    numbers_count = 0
    strangechar_count = 0

    for letter in password:

        letters_errormessage = "minimo 4 letras"
        numbers_errormessage = "minimo 2 números"
        strangechar_errormessage = "minimo 2 caracteres adicionales"

        if letter in letters:
            letters_count += 1
        elif letter in numbers:
            numbers_count += 1
        elif letter in strangechar:
            strangechar_count += 1
        
    letters_flag = False
    numbers_flag = False
    strangecharcount = False

    error_list = []

    if letters_count >= 4:
        letters_flag = True
    else:
        error_list.append(letters_errormessage)

    if numbers_count >= 2:
        numbers_flag = True
    else:
        error_list.append(numbers_errormessage)

    if strangechar_count >= 2:
        strangechar_flag = True
    else:
        error_list.append(strangechar_errormessage)

    if letters_flag and numbers_flag and strangechar_flag:
        return [True, ""]

    else:
        return [False, error_list]
            

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2') #Confirmar contraseña

        passflag, passerrors = passwordcheck(password)

        #Exigencias de contraseña (Quizas hacerla mas segura, min 8 caracteres, maximo 15)
        #Verificación
        if username is not None and password is not None and passflag:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Este usuario ya existe, intentelo de nuevo")
                else:
                    User.objects.create_user(username=username, password=password)
                    messages.success(request, "Bienvenido a FOCUSTOM")
                    return redirect('login') #Redirige a Login
            else:
                messages.error(request, "Las contraseñas no coinciden")

    return render(request, "register_page.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        flag1 = False
        flag2 = False

    #Primero revisa las 2 cosas antes de informar un error
        if username is not None and password is not None:
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