from dashboard.utils.finder import Finder
import requests


class Series(Finder):
    def search_series(self, query):
        # search and get the response
        resp = requests.get(self.tmdb_series_website.replace("[query]", query)).json()[
            "results"
        ]

        return resp