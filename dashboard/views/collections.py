from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from dashboard.forms.collections import AddCollectionForm
from dashboard.models.collections import Collections

from nanoid import generate

## Dashboard > Collections View
@method_decorator(login_required, name="dispatch")
class CollectionsView(View):
    form_class = AddCollectionForm
    template_name = "main/collections.html"

    # GET request
    def get(self, request, *args, **kwargs):
        collections = Collections.objects.order_by("-date_created")

        return render(
            request,
            self.template_name,
            {"form": self.form_class, "collections": collections},
        )

    # generate a slug for the collection
    def generate_slug(self):
        slug = generate(size=6)  # generate from nanoid

        # query the slug if it already exists
        check = Collections.objects.filter(slug=slug)
        if check:
            return self.generate_slug()

        # if it does not exist, return the slug
        return slug

    # POST request
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # generate and get the slug
            slug = self.generate_slug()

            # add new collection to the database
            Collections.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                slug=slug,
            )

            messages.success(request, "Succesfully created new collection!")
            return redirect("collections")


class CollectionsPageView(View):
    pass