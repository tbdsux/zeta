from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# dashboard index
@login_required()
def index(request):
    return render(request, "main/index.html")


# user logout
def Logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("login")
