from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User

# import custom update forms
from dashboard.forms.account import UpdateUserInfo


class AccountSettingsView(View):
    form_class = UpdateUserInfo
    template_name = "main/settings.html"

    def get(self, request, *args, **kwargs):
        # get the user info
        user = User.objects.get(username=request.user)

        # pass username and password to the user info form
        form = self.form_class(initial={"username": user.username, "email": user.email})

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request, *args, **kwargs):
        # query the user info
        user = User.objects.get(username=request.user)

        # check and validate form
        form = self.form_class(request.POST)
        if form.is_valid():
            # get each post data
            fusername = form.cleaned_data["username"]
            femail = form.cleaned_data["email"]
            fpassword = form.cleaned_data["password"]

            # save each data if exists and not similar to existing info
            if fusername and fusername != user.username:
                user.username = fusername
            if femail and femail != user.email:
                user.email = femail
            if fpassword:
                user.password = fpassword

            # update to the db
            user.save()

            # add success message
            messages.success(request, "Successfully updated account settings!")

            # redirect to similar page
            return redirect("account")
