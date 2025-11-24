from django.shortcuts import render, redirect
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
from .models import user_notes
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import os
from io import BytesIO
from django.urls import reverse
from django.views.decorators.http import require_POST
# librerias de google:
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


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
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url='login')
@xframe_options_exempt
def user_notes_view(request):
    user = request.user
    note_obj, created = user_notes.objects.get_or_create(user=user)

    if request.method == "POST":
        content = request.POST.get("user_note", "")
        note_obj.user_notes = content
        note_obj.save()
        return redirect('notes')

    return render(request, "notes.html", {"note": note_obj})

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
                    hour=display_time,
                    half=half
                ).first()


                row[day] = block.task_name if block else ""

            schedule_table.append(row)

    return render(request, "schedule.html", {"schedule_table": schedule_table})

@login_required(login_url='login')
@xframe_options_exempt
def timer(request):
    return render(request, 'timer.html')

@login_required(login_url='login')
@xframe_options_exempt
def drive(request):
    return render(request, 'ventdrive.html')

def cuadrantes_view(request):
    return render(request, 'home.html')

#FUNCIONES DRIVE:
# Para desarrollo local
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = ['https://www.googleapis.com/auth/drive.file']
REDIRECT_URI = 'http://127.0.0.1:8000/gdrive/auth/callback/'

def launcher(request):
    return render(request, "launcher.html")

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def drive_login(request):
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    request.session['state'] = state
    return redirect(authorization_url)

import requests
from django.shortcuts import redirect

def drive_logout(request):
    creds = request.session.get("credentials")

    if creds:
        token = creds.get("token")
        requests.post(
            'https://oauth2.googleapis.com/revoke',
            params={'token': token},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )

    request.session.pop("credentials", None)
    
    return redirect("home")  # o donde quieras

def drive_callback(request):
    state = request.session.get("state")

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )

    # Obtener token
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    #refresh_token
    stored = request.session.get("credentials")

    # Si NO hay refresh_token en sesión pero Google entrega uno: se guarda
    if credentials.refresh_token:
        request.session["credentials"] = credentials_to_dict(credentials)

    # Si Google NO dio refresh_token (normal después del primer login),
    # conserva el antiguo para evitar el RefreshError.
    else:
        if stored and stored.get("refresh_token"):
            creds_dict = credentials_to_dict(credentials)
            creds_dict["refresh_token"] = stored["refresh_token"]
            request.session["credentials"] = creds_dict
        else:
            # Caso raro
            request.session["credentials"] = credentials_to_dict(credentials)

    return redirect("gdrive_view")

@xframe_options_exempt
def drive_view(request):
    # Si no hay credenciales, pedir login
    if 'credentials' not in request.session:
        return redirect('gdrive_login')

    creds_dict = request.session['credentials']
    creds = google.oauth2.credentials.Credentials(**creds_dict)

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        pageSize=50,
        fields="files(id, name, mimeType, webViewLink, webContentLink)"
    ).execute()

    files = results.get('files', [])
    return render(request, "drive.html", {"files": files})

@require_POST
def upload_file_to_drive(request):
    if 'credentials' not in request.session:
        return redirect('gdrive_login')

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return redirect('gdrive_view')

    creds_dict = request.session['credentials']
    creds = google.oauth2.credentials.Credentials(**creds_dict)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': uploaded_file.name}
    file_stream = BytesIO()
    for chunk in uploaded_file.chunks():
        file_stream.write(chunk)
    file_stream.seek(0)

    media = MediaIoBaseUpload(file_stream, mimetype=uploaded_file.content_type)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return redirect('gdrive_view')

@xframe_options_exempt
def accessdrive(request):
    return render(request, "accessdrive.html")