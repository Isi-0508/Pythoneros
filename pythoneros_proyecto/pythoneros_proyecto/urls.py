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
from myapp import views as myapp_views
from Users import views as Users_views
from home import views as home_views

urlpatterns = [
    # path('', views.myapp, name='myapp'),
    path('myapp/', myapp_views.myapp, name='myapp'),
    path('admin/', admin.site.urls),
    path('home/', home_views.home, name='home'),
    path('login/', Users_views.login, name='login'),
    # path('logout/', views.home, name='logout'),
    path('register/', Users_views.register, name='register'),
]
