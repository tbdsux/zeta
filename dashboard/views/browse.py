from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from dashboard.forms.browse import BrowseForm

## Dashboard > Browse View
@method_decorator(login_required, name="dispatch")
class BrowseView(View):
    form_class = BrowseForm
    template_name = "main/browse.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pass


## Dashboard > Browse > Query results View
@method_decorator(login_required, name="dispatch")
class BrowseResultsView(View):
    template_name = "main/search_output.html"

    def get(self, request, query, *args, **kwargs):
        return render(request, self.template_name)