from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from dashboard.models import UserProfile

# main index
def index(request):
    return render(request, "front/index.html")


# register form
def Register(request):
    # redirect if already logged in
    if request.user.is_authenticated:
        return redirect("dash")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save the login information
            user = form.save()
            # generate and save a UserProfile
            profile = UserProfile(user=user)
            profile.save()

            # show the success message
            messages.success(request, "Your account has been successfully created!")
            return redirect("login")

    form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def Login(request):
    # redirect if already logged in
    if request.user.is_authenticated:
        return redirect("dash")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # login the user
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("dash")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = LoginForm()
    return render(request, "registration/login.html", {"form": form})
