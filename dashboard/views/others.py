from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


# user logout
def Logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("login")
