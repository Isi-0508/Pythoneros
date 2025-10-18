from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

#(!) CORREGIR
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
strangechar = "!@#$%^&*()-_=+[];:,.<>/?"

#La contraseña debe contener al menos:
#-8 caracteres, de ellos:
# 4 letras, 2 numeros y 2 caracteres raros
#LOGIN/REGISTER

#Retirar lista de errores
def passwordcheck(password):
    letters_count = 0
    numbers_count = 0
    strangechar_count = 0
    not_usable_password = "abcd12%$"

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
    strangechar_flag = False
    notusable_password_flag = False

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

    if password != not_usable_password:
        notusable_password_flag = True

    if letters_flag and numbers_flag and strangechar_flag and notusable_password_flag:
        return [True, ""]

    else:
        return [False, error_list]

# LOGIN RECQUIRED.

# (!) COMPLETADO
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2') #Confirmar contraseña

        passflag, passerrors = passwordcheck(password)

        #Verificación
        if username is not None and password is not None and passflag:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "(!) Este usuario ya existe, intentelo de nuevo")
                else:
                    User.objects.create_user(username=username, password=password)
                    messages.success(request, "Bienvenido a FOCUSTOM")
                    return redirect('login') #Redirige a Login
            else:
                messages.error(request, "(!) Las contraseñas no coinciden")
        # elif not passflag:

    return render(request, "register_page.html")

# (!) COMPLETADO
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #auth_login esta llamada de otra forma
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {username}!")
            return redirect('home') #redirige a home
        else:
            messages.error(request, "(!) Usuario o Contraseña Incorrectos, intentelo nuevamente")

    return render(request,"login_page.html")

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    '''
    #Cambio de Nombre de Usuario:
    if request.method == "POST":
        new_username = request.POST.get('newusername')
    #Cambio de Contraseña:
    if request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2') #Confirmar contraseña

        passflag, passerrors = passwordcheck(password)
    '''

    return render(request, "profile_page_index.html")

#CONTRASEÑA FUNCIONAL 100%
# efgh34%$