from dashboard.utils.finder import Finder
import requests


class Manga(Finder):
    def search_manga(self, query):
        # search and get the response
        resp = requests.get(self.manga_jikan.replace("[query]", query)).json()[
            "results"
        ]

        return resp