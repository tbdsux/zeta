from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from dashboard.models.collections import Collections, Stuff

## Dashboard > Index (Main) View
@method_decorator(login_required, name="dispatch")
class IndexDashboardView(View):
    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        # query the collections
        collections = Collections.objects.all()

        # query each type
        movies = collections.filter(type="movie")
        series = collections.filter(type="series")
        animes = collections.filter(type="anime")
        books = collections.filter(type="book")
        mangas = collections.filter(type="manga")
        asian_dramas = collections.filter(type="asian drama")

        # render
        return render(
            request,
            self.template_name,
            {
                "col_count": collections.count(),
                "movies": movies,
                "series": series,
                "animes": animes,
                "books": books,
                "mangas": mangas,
                "asian_dramas": asian_dramas,
            },
        )
