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
import uuid
from dashboard.utils.browse.movies import Movies
from dashboard.utils.browse.series import Series
from dashboard.utils.browse.anime import Anime
from dashboard.utils.browse.manga import Manga
from dashboard.utils.browse.asian_drama import AsianDrama
from dashboard.utils.browse.book import Book

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


## Dashboard > Update Collections Info
@method_decorator(login_required, name="dispatch")
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


## Dashboard > Remove a Collection
@method_decorator(login_required, name="dispatch")
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


## Dashboard > Page of Each Collections
@method_decorator(login_required, name="dispatch")
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


## Dashboard > Finding and Adding a New Item to a Collection
@method_decorator(login_required, name="dispatch")
class CollectionsFindItemView(View):
    form_class = AddItemCollection
    template_name = {
        "movie": "main/collections/add-item-movies.html",
        "series": "main/collections/add-item-series.html",
        "anime": "main/collections/add-item-anime.html",
        "manga": "main/collections/add-item-manga.html",
        "asian_drama": "main/collections/add-item-asian.html",
        "book": "main/collections/add-item-book.html",
    }

    def get(self, request, slug, type, query, *args, **kwargs):
        # movies collections
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

        # series collections
        elif type == "series":
            # search the series with the api
            find = Series()
            results = find.search_series(query)

            # render the results
            return render(
                request,
                self.template_name["series"],
                {"slug": slug, "query": query, "results": results, "type": "series"},
            )

        # anime collections
        elif type == "anime":
            # search the anime with the api
            find = Anime()
            results = find.search_anime(query)

            # render the results
            return render(
                request,
                self.template_name["anime"],
                {"slug": slug, "query": query, "results": results, "type": "anime"},
            )

        # manga collections
        elif type == "manga":
            # search the manga with the api
            find = Manga()
            results = find.search_manga(query)

            # render the results
            return render(
                request,
                self.template_name["manga"],
                {"slug": slug, "query": query, "results": results, "type": "manga"},
            )

        # asian drama collections
        elif type == "asian-drama":
            # search the asian drama with the api
            find = AsianDrama()
            results = find.search_asian(query)

            # render the results
            return render(
                request,
                self.template_name["asian_drama"],
                {
                    "slug": slug,
                    "query": query,
                    "results": results,
                    "type": "asian drama",
                },
            )

        # book collections
        elif type == "book":
            # search the book with the api
            find = Book()
            results = find.search_book(query)

            # render the results
            return render(
                request,
                self.template_name["book"],
                {
                    "slug": slug,
                    "query": query,
                    "results": results,
                    "type": "asian drama",
                },
            )

    def generate_uuid(self, slug):
        # generate the uuid
        uid = uuid.uuid4()

        # check if the id exists in the collection
        check = Stuff.objects.filter(collections__slug=slug).filter(stuff_uid=uid)
        if check:
            return self.generate_uuid()

        return uid

    def post(self, request, *args, **kwargs):
        # get and verify first the slugid
        slug = request.POST["slugid"]
        collection = Collections.objects.filter(slug=slug).filter(owner=request.user)[0]
        uid = self.generate_uuid(slug)

        if collection:
            # create stuff item
            item = Stuff.objects.create(
                title=request.POST["title"],
                img_src=request.POST["img"],
                classification=request.POST["type"],
                stuff_uid=uid,
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


## Dashboard > Removing an Item from the Collection
@method_decorator(login_required, name="dispatch")
class CollectionsRemoveItemView(View):
    template_name = "main/collections/delete-item.html"

    def get(self, request, slug, stuff_id, *args, **kwargs):
        # get the collection info
        collection = Collections.objects.filter(owner=request.user).get(slug=slug)
        # get the stuff info
        stuff = collection.stuffs.get(stuff_uid=stuff_id)

        if stuff and collection:
            return render(
                request, self.template_name, {"item": stuff, "collection": collection}
            )

    def post(self, request, *args, **kwargs):
        # get the slug
        slug = request.POST["slugid"]
        # verify the slug and stuffid
        stuff = Stuff.objects.filter(collections__slug=slug).get(
            stuff_uid=request.POST["stuffid"]
        )
        if stuff:
            # get the collection
            collection = Collections.objects.filter(owner=request.user).get(slug=slug)

            # remove the stuff from the collection
            collection.stuffs.remove(stuff)

            # success message
            messages.success(request, "Successfully removed item!")

            # redirect to the collections page
            return redirect("collections-page", slug=slug)
