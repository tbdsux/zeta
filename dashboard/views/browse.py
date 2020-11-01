from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

## Dashboard > Browse View
@method_decorator(login_required, name="dispatch")
class BrowseView(View):
    template_name = "main/browse.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_namee)