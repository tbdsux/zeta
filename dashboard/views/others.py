from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from dashboard.forms.account import UpdatePasswordForm


# user logout
def Logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("login")
