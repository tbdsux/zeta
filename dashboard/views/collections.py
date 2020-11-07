from django.http import request
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from dashboard.forms.collections import (
    AddCollectionForm,
    UpdateCollectionForm,
    AddItemCollection,
)
from dashboard.models.collections import Collections, Stuff, Inclution

# utilities
from nanoid import generate
from dashboard.utils.browse.movies import Movies

## Dashboard > Collections View
@method_decorator(login_required, name="dispatch")
class CollectionsView(View):
    form_class = AddCollectionForm
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
    form_class = UpdateCollectionForm
    template_name = "main/collections/collections_edit.html"

    def get(self, request, slug, *args, **kwargs):
        # query the slug collection
        collection = Collections.objects.filter(slug=slug).filter(owner=request.user)[0]
        if collection:
            # pass values to the form fields
            form = self.form_class(
                initial={
                    "name": collection.name,
                    "type": collection.type,
                    "description": collection.description,
                }
            )

            return render(
                request,
                self.template_name,
                {"collection": collection, "form": form},
            )

    def post(self, request, *args, **kwargs):
        # verify the collection id
        col = Collections.objects.get(collection_id=request.POST["colid"])
        if col:
            # verify the form
            form = self.form_class(request.POST)
            if form.is_valid():
                # update each field
                if form.cleaned_data["name"]:
                    col.name = form.cleaned_data["name"]
                if form.cleaned_data["type"]:
                    col.type = form.cleaned_data["type"]
                if form.cleaned_data["description"]:
                    col.description = form.cleaned_data["description"]

                # update the collection info
                col.save()

                # success message
                messages.success(request, "Successfully updated collection!")

                # redirect to the collectons
                return redirect("collections")


class CollectionsDeleteView(View):
    template_name = "main/collections/collections_delete.html"

    def get(self, request, slug, *args, **kwargs):
        # query the slug id
        collection = Collections.objects.filter(slug=slug).filter(owner=request.user)

        if collection:
            return render(request, self.template_name, {"collection": collection[0]})

    def post(self, request, *args, **kwargs):
        # query and verify the slug
        check = Collections.objects.filter(slug=request.POST["slug"]).filter(
            owner=request.user
        )
        if check:
            # remove the collection
            check.delete()

            # show the success message
            messages.success(request, f"Successfully removed collection!")

            # redirect back to the collections page
            return redirect("collections")


class CollectionsPageView(View):
    form_class = AddItemCollection
    template_name = "main/collections/collections_page.html"

    def get(self, request, slug, *args, **kwargs):
        # get the collection from the slug
        collection = Collections.objects.filter(owner=request.user).get(slug=slug)

        if collection:
            # pass initial values to hidden inputs
            form = self.form_class(
                initial={
                    "slugid": collection.slug,
                    "type": collection.type.replace(" ", "-"),
                }
            )

            return render(
                request,
                self.template_name,
                {
                    "collection": collection,
                    "form": form,
                    "items": collection.stuffs.order_by("-id"),
                },
            )

    def post(self, request, *args, **kwargs):
        # get the post data
        form = self.form_class(request.POST)

        if form.is_valid():
            return redirect(
                "collections-add-item",
                slug=form.cleaned_data["slugid"],
                type=form.cleaned_data["type"],
                query=form.cleaned_data["query"],
            )


class CollectionsFindItemView(View):
    template_name = {"movie": "main/collections/add-item-movies.html"}

    def get(self, request, slug, type, query, *args, **kwargs):
        if type == "movie":
            # search the movies with the api
            find = Movies()
            results = find.search_movies(query)

            # render the results
            return render(
                request,
                self.template_name["movie"],
                {"slug": slug, "query": query, "results": results, "type": "movie"},
            )

    def post(self, request, *args, **kwargs):
        # get and verify first the slugid
        slug = request.POST["slugid"]
        collection = Collections.objects.filter(slug=slug).filter(owner=request.user)[0]

        if collection:
            # create stuff item
            item = Stuff.objects.create(
                title=request.POST["title"],
                img_src=request.POST["img"],
                classification=request.POST["type"],
            )

            # add to inclusion
            Inclution.objects.create(
                user=request.user,
                collection=collection,
                stuff=item,
                added_to=slug,
            )

            # add success message
            messages.success(request, "Successfully added new item!")

            # redirect back to the collections page
            return redirect("collections-page", slug=slug)
