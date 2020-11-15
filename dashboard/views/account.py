from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# import custom update forms
from dashboard.forms.account import (
    UpdateUserInfoUsername,
    UpdateUserInfoEmail,
    UpdatePasswordForm,
)


## Dashboard > Accounts Settings View
@method_decorator(login_required, name="dispatch")
class AccountSettingsView(View):
    form_class = {"username": UpdateUserInfoUsername, "email": UpdateUserInfoEmail}
    template_name = "main/settings.html"

    def get(self, request, *args, **kwargs):
        uname_form = self.form_class["username"](
            request.user,
            initial={"username": request.user.username, "action": "username"},
        )
        email_form = self.form_class["email"](
            request.user,
            initial={"email": request.user.email, "action": "email"},
        )

        return render(
            request,
            self.template_name,
            {"uname_form": uname_form, "email_form": email_form},
        )

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]

        if action in ["username", "email"]:
            form = self.form_class[action](request.user, data=request.POST)
            print(action)
            print(form.is_valid())
            if form.is_valid():
                form.save()

                messages.success(
                    request, f"You have successfully updated your {action}!"
                )

                return redirect("account")

        uname_form = self.form_class["username"](
            request.user,
            initial={"username": request.user.username, "action": "username"},
        )
        email_form = self.form_class["email"](
            request.user,
            initial={"email": request.user.email, "action": "email"},
        )

        return render(
            request,
            self.template_name,
            {"uname_form": uname_form, "email_form": email_form},
        )


@login_required()
def Account_Settings(request):
    uname_form = UpdateUserInfoUsername(
        request.user,
        initial={"username": request.user.username, "action": "username"},
    )
    email_form = UpdateUserInfoEmail(
        request.user,
        initial={"email": request.user.email, "action": "email"},
    )

    if request.method == "POST":
        action = request.POST["action"]
        if action == "username":
            uname_form = UpdateUserInfoUsername(request.user, data=request.POST)
            if uname_form.is_valid():
                uname_form.save()

                messages.success(
                    request, f"You have successfully updated your username!"
                )

                return redirect("account")

        elif action == "email":
            email_form = UpdateUserInfoEmail(request.user, data=request.POST)
            if email_form.is_valid():
                email_form.save()

                messages.success(
                    request, f"You have successfully updated your email address!"
                )

                return redirect("account")

    return render(
        request,
        "main/settings.html",
        {"uname_form": uname_form, "email_form": email_form},
    )


## Dashboard > Change Password View
@method_decorator(login_required, name="dispatch")
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = UpdatePasswordForm
    template_name = "main/change_password.html"
    success_url = reverse_lazy("account-password")
    success_message = "Your password have been successfully updated!"