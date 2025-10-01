from django.shortcuts import render
from django.http import HttpResponse

def myapp(request):
    return HttpResponse("Hola mundo")
# Create your views here.
def home(request):
    return render(request,"home.html")