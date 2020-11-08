from dashboard.utils.finder import Finder
import requests


class Anime(Finder):
    def search_anime(self, query):
        # search and get the response
        resp = requests.get(self.anime_jikan.replace("[query]", query)).json()[
            "results"
        ]

        return resp