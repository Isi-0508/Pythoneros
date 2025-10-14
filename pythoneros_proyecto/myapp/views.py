from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

def myapp(request):
    return HttpResponse("The Walten Files")

# Create your views here.