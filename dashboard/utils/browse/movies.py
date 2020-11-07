from dashboard.utils.finder import Finder
import requests


class Movies(Finder):
    def search_movies(self, query):
        # search and get the response
        resp = requests.get(self.tmdb_movie_website.replace("[query]", query)).json()[
            "results"
        ]

        return resp