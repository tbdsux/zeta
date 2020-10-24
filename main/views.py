from django.shortcuts import render
from django.http import HttpResponse

# main index 
def index(request):
    return render(request, "front/index.html")

# register form
def register(request):
    return render(request, "forms/register.html")

# login form
def login(request):
    return render(request, "forms/login.html")