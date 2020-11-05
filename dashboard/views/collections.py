from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from dashboard.forms.collections import AddUpdateCollectionForm
from dashboard.models.collections import Collections

from nanoid import generate

## Dashboard > Collections View
@method_decorator(login_required, name="dispatch")
class CollectionsView(View):
    form_class = AddUpdateCollectionForm
    template_name = "main/collections/collections.html"

    # GET request
    def get(self, request, *args, **kwargs):
        collections = Collections.objects.filter(owner=request.user).order_by(
            "-date_created"
        )

        return render(
            request,
            self.template_name,
            {"form": self.form_class, "collections": collections},
        )

    # generate a slug for the collection
    def generate_slug(self, user):
        slug = generate(size=7)  # generate from nanoid

        # query the slug if it already exists
        # slugs can be similar with different users but not with single user
        check = Collections.objects.filter(slug=slug).filter(owner=user)
        if check:
            return self.generate_slug()

        # if it does not exist, return the slug
        return slug

    # generate the collection id
    def generate_col_id(self):
        colid = int(generate("1234567890", 19))

        # query the id if it already exists
        # the id must be different from everything
        check = Collections.objects.filter(collection_id=colid)
        if check:
            return self.generate_col_id()

        # if the id does not exist, return it
        return colid

    # POST request
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # generate and get the slug
            slug = self.generate_slug(request.user)

            # generate and get the collection id
            colid = self.generate_col_id()

            # add new collection to the database
            Collections.objects.create(
                owner=request.user,
                name=form.cleaned_data["name"],
                collection_id=colid,
                description=form.cleaned_data["description"],
                type=form.cleaned_data["type"],
                slug=slug,
            )

            messages.success(request, "Succesfully created new collection!")
            return redirect("collections")


class CollectionsUpdateView(View):
    form_class = AddUpdateCollectionForm
    template_name = "main/collections/collections_edit.html"

    def get(self, request, slug, *args, **kwargs):
        # get the slug id of the collection
        return render(request, self.template_name)


class CollectionsPageView(View):
    template_name = "main/collections/collections_page.html"

    def get(self, request, slug, *args, **kwargs):
        # get the collection from the slug
        collection = Collections.objects.filter(owner=request.user).get(slug=slug)

        return render(request, self.template_name, {"collection": collection})