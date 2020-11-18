from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from dashboard.models.collections import Collections, Stuff, Inclution
import uuid
from urllib.parse import quote, unquote  # for url encoding and decoding

from dashboard.forms.browse import BrowseForm
from dashboard.utils.browse.movies import Movies
from dashboard.utils.browse.series import Series
from dashboard.utils.browse.anime import Anime
from dashboard.utils.browse.book import Book
from dashboard.utils.browse.manga import Manga
from dashboard.utils.browse.asian_drama import AsianDrama
from dashboard.utils.hasher import Hasher

## Dashboard > Browse View
@method_decorator(login_required, name="dispatch")
class BrowseView(View):
    form_class = BrowseForm
    template_name = "main/browse/browse.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return redirect(
                "browse-results",
                type=form.cleaned_data["type"],
                query=form.cleaned_data["query"],
            )

        return render(request, self.template_name, {"form": form})


## Dashboard > Browse > Query results View
@method_decorator(login_required, name="dispatch")
class BrowseResultsView(View):
    form_class = BrowseForm
    template_name = "main/browse/search_output.html"

    def get(self, request, type, query, *args, **kwargs):
        # set values to form
        form = self.form_class(initial={"type": type.replace("-", " "), "query": query})

        result = {}

        # query from the apis
        if type == "movie":
            finder = Movies()
            result = finder.search_movies(query)
        elif type == "series":
            finder = Series()
            result = finder.search_series(query)
        elif type == "anime":
            finder = Anime()
            result = finder.search_anime(query)
        elif type == "book":
            finder = Book()
            result = finder.search_book(query)
        elif type == "manga":
            finder = Manga()
            result = finder.search_manga(query)
        elif type == "asian-drama":
            finder = AsianDrama()
            result = finder.search_asian(query)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "type": type.replace("-", " "),
                "query": query,
                "results": result,
            },
        )

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]

        # results form, search again
        if action == "browse-search":
            form = self.form_class(request.POST)
            if form.is_valid():
                return redirect(
                    "browse-results",
                    type=form.cleaned_data["type"],
                    query=form.cleaned_data["query"],
                )

        # adding new item from the results to a collection
        elif action == "add-item":
            data = {
                "title": request.POST["title"],
                "img": request.POST["img"],
            }

            hashed = Hasher.hash(data)

            return redirect(
                "browse-add-item",
                type=request.POST["type"].replace(" ", "-"),
                hash=quote(hashed, safe=""),
            )

        # redirect (add error in the future)
        return redirect(request.path_info)


## Dashboard > Browse > Add item to collection
@method_decorator(login_required, name="dispatch")
class BrowseAddResultCol(View):
    template_name = "main/browse/select-collection.html"

    def get(self, request, type, hash, *args, **kwargs):
        # query all user collections from type
        collections = Collections.objects.filter(owner=request.user).filter(
            type=type.replace("-", " ")
        )

        # decode the hash
        data = Hasher.decode(unquote(hash))

        return render(
            request,
            self.template_name,
            {"collections": collections, "data": data, "type": type},
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
        # get all post data
        slug = request.POST["slugid"]
        type = request.POST["type"]
        title = request.POST["title"]
        img = request.POST["img"]

        # check if all exists
        if slug and type and title and img:
            # query collection info
            collection = Collections.objects.filter(slug=slug).filter(
                owner=request.user
            )[0]
            uid = self.generate_uuid(slug)

            if collection:
                # create stuff item
                item = Stuff.objects.create(
                    title=title,
                    img_src=img,
                    classification=type,
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
