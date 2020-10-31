from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from .forms import AddCollectionForm
from .models import Collections

## Dashboard > Collections View
@method_decorator(login_required, name="dispatch")
class CollectionsView(View):
    form_class = AddCollectionForm
    template_name = "main/collections.html"

    def get(self, request, *args, **kwargs):
        collections = Collections.objects.all()

        return render(
            request,
            self.template_name,
            {"form": self.form_class, "collections": collections},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # add new collection to the database
            Collections.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
            )

            messages.success(request, "Succesfully created new collection!")
            return redirect("collections")


# dashboard index
@login_required()
def index(request):
    return render(request, "main/index.html")


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
