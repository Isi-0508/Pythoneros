from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

# Create your views here.

#(!) CORREGIR
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
strangechar = "!@#$%^&*()-_=+[];:,.<>/?"

#La contraseña debe contener al menos:
#-8 caracteres, de ellos:
# 4 letras, 2 numeros y 2 caracteres raros
#LOGIN/REGISTER

#Retirar lsita de errores
#Corregir limites

# (!) COMPLETADO
def passwordcheck(password):
    letters_count = 0
    numbers_count = 0
    strangechar_count = 0
    not_usable_password = "abcd12%$"

    for letter in password:

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
    len_flag = False

    if 10 >= len(password) >= 8:
        len_flag = True
    
    if letters_count >= 4:
        letters_flag = True

    if numbers_count >= 2:
        numbers_flag = True

    if strangechar_count >= 2:
        strangechar_flag = True

    if password != not_usable_password:
        notusable_password_flag = True



    if letters_flag and numbers_flag and strangechar_flag and notusable_password_flag:
        return True

    else:
        return False



# (!) COMPLETADO
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2') #Confirmar contraseña

        passflag = passwordcheck(password)

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
                messages.error(request, "(!) Las contraseñas no coinciden, intentelo de nuevo")
        # elif not passflag:

    return render(request, "register_page.html")

# (!) COMPLETADO
def login(request):
    if request.user.is_authenticated:
        return redirect('home')

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

# (!) COMPLETADO
@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

# (!) COMPLETADO
@login_required(login_url='login')
def profile(request):
    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")

        #Cambio de Nombre de Usuario:
        if action == 'changeusername':
            new_username = request.POST.get('newusername')

            if new_username is not None:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, "(!) Este nombre de usuario ya esta en uso.")
                else:
                    user.username = new_username
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Nombre de usuario actualizado con exito.")
                    return redirect ('profile')
            else:
                messages.error(request, "(!) Nombre de usuario no valido, intentelo de nuevo")



        #Cambio de Contraseña:
        elif action == 'changepassword':
            if request.method == "POST":
                oldpassword = request.POST.get('oldpassword')
                newpassword = request.POST.get('newpassword')
                newpassword2 = request.POST.get('newpassword2') #Confirmar contraseña
                
                passflag = passwordcheck(newpassword)

                oldpasswordflag = authenticate(request, username=request.user.username, password=oldpassword)

                #Verificación
                if oldpassword is not None and newpassword is not None and newpassword2 is not None:
                    if oldpasswordflag is not None :
                        if oldpassword != newpassword:
                            if passflag:
                                if newpassword == newpassword2:
                                    user.set_password(newpassword)
                                    user.save()
                                    update_session_auth_hash(request, user)
                                    messages.success(request, "Contraseña actualizada con exito")
                                else:
                                    messages.error(request, "(!) Las contraseñas no coinciden, intentelo de nuevo")
                            else:
                                messages.error(request, "(!) Contraseña nueva no valida, intentelo de nuevo")
                        else:
                            messages.error(request, "(!) Su contraseña nueva no puede ser la misma que su anterior contraseña, intentelo de nuevo")
                    else:
                        messages.error(request, "(!) Contraseña vieja incorrecta")
                else:
                    messages.error(request, "(!) Los datos ingresados no son validos, intentelo de nuevo") #Esta linea es inutil

    return render(request,"profile_page_index.html")

#CONTRASEÑA FUNCIONAL 100%
# efgh34%$