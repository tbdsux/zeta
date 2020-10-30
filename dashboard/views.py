from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile


# dashboard index
@login_required()
def index(request):
    return render(request, "main/index.html")


# dashboard collections
@login_required()
def collections(request):
    return render(request, "main/collections.html")


# dashboard browse
@login_required()
def browse(request):
    return render(request, "main/browse.html")


# user profile
def profile(request):
    return render(request, "main/profile.html")


# user logout
def Logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("login")
