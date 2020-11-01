from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class AccountSettingsView(View):
    template_name = "main/settings.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)