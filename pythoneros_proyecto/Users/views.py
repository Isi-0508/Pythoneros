from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

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
        email = request.POST.get('mail')
        password = request.POST.get('password')
        password2 = request.POST.get('password2') #Confirmar contraseña

        passflag = passwordcheck(password)

        #Verificación
        if username is not None and password is not None and passflag:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "(!) Este usuario ya existe, intentelo de nuevo")
                else:
                    User.objects.create_user(username=username, password=password, email=email)
                    messages.success(request, "Bienvenido a Piwit")
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




User = get_user_model()
# (!) COMPLETADO

@login_required(login_url='login')
def profile(request):
    user = request.user

    if request.method == "POST":
        new_username = (request.POST.get("username") or "").strip()
        new_email    = (request.POST.get("email") or "").strip()
        old_pwd      = request.POST.get("old_password") or ""
        new_pwd      = request.POST.get("new_password") or ""
        new_pwd2     = request.POST.get("new_password2") or ""

        changed_any = False

        # --- Cambio de username ---
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, "(!) Ese nombre de usuario ya está en uso.")
            else:
                user.username = new_username
                changed_any = True
                messages.success(request, "Nombre de usuario actualizado con éxito.")

        # --- Cambio de email ---
        if new_email and new_email != user.email:
            try:
                validate_email(new_email)
            except ValidationError:
                messages.error(request, "(!) Correo electrónico inválido.")
            else:
                if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                    messages.error(request, "(!) Ese correo ya está en uso.")
                else:
                    user.email = new_email
                    changed_any = True
                    messages.success(request, "Correo electrónico actualizado con éxito.")

        # --- Cambio de contraseña ---
        if new_pwd or new_pwd2:
            if not old_pwd:
                messages.error(request, "(!) Debes ingresar tu contraseña actual para cambiarla.")
            elif not authenticate(username=user.username, password=old_pwd):
                messages.error(request, "(!) La contraseña actual es incorrecta.")
            elif not new_pwd or not new_pwd2:
                messages.error(request, "(!) Ingresa y confirma la nueva contraseña.")
            elif new_pwd != new_pwd2:
                messages.error(request, "(!) Las contraseñas no coinciden.")
            elif new_pwd == old_pwd:
                messages.error(request, "(!) La nueva no puede ser igual a la actual.")
            else:
                if passwordcheck(new_pwd):
                    user.set_password(new_pwd)
                    changed_any = True
                    messages.success(request, "Contraseña actualizada con éxito.")
                    update_session_auth_hash(request, user)
                else:
                    messages.error(
                        request,
                        "(!) La nueva contraseña no cumple los requisitos mínimos (La contraseña debe contener al menos: 8 caracteres, de ellos: 4 letras, 2 numeros y 2 caracteres raros)"
                    )

        # --- Guardar si hubo cambios válidos ---
        if changed_any:
            user.save()
            return redirect("profile")

        # Si no hubo cambios ni errores
        if not any(m.level_tag == "error" for m in messages.get_messages(request)):
            messages.info(request, "No hiciste cambios. Todo quedó igual.")
            return redirect("profile")
    return render(request, "profile_page_index.html")



@login_required(login_url='login')
def deleteacc(request):
    user = request.user

    if request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if user.check_password(password):
            if password == password2:
                user.delete()
                auth_logout(request)
                messages.success(request, "¡Cuenta eliminada con exito, gracias por ser parte de Piwit!")
                return redirect('login')
            else:
                messages.error(request, "(!) Las contraseñas no coinciden, intentelo de nuevo")

        else:
            messages.error(request, "(!) Contraseña incorrecta, intentelo de nuevoA")

    return render(request, "deleteacc_page.html")


#CONTRASEÑA FUNCIONAL 100%
# efgh34%$