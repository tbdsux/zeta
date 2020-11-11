from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages


# user logout
def Logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("login")
