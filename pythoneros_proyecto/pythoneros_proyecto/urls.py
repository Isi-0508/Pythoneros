"""
URL configuration for pythoneros_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from Users import views
from Users import views as Users_views
from Main import views as Main_views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),

    #MAIN
    path('home/', Main_views.home, name='home'),
    path('journal/', Main_views.journal, name='journal'),
    path('timer/', Main_views.timer, name='timer'),
    path('pomodoro/', Main_views.iniciar_pomodoro, name='pomodoro'), #PROVISORIO
    path('cuadrantes/', Main_views.cuadrantes_view, name='cuadrantes'),#PROVISORIO
    path('pomodoro/aumentar/', Main_views.aumentar_sesiones, name='aumentar_sesiones'),#PROVISORIO
    path('pomodoro/disminuir/', Main_views.disminuir_sesiones, name='disminuir_sesiones'),#PROVISORIO
    path('drive', Main_views.drive, name='drive'),
    path('notes/', Main_views.user_notes_view, name='notes'),

    #USERS
    path('login/', Users_views.login, name='login'),
    path('logout/', Users_views.logout, name='logout'),
    path('register/', Users_views.register, name='register'),
    path('deleteacc/', Users_views.deleteacc, name='deleteacc'),
    path('profile/', Users_views.profile, name='profile'),

    #MISCELLEANOUS
    path('about/', Main_views.about, name='about'),


    path("choose-avatar/", views.choose_avatar, name="choose_avatar"),
    path("set-avatar/", views.set_avatar, name="set_avatar"),

]
