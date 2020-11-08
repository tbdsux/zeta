from dashboard.utils.finder import Finder
import requests


class Book(Finder):
    def search_book(self, query):
        # search and get the response
        resp = requests.get(self.open_library.replace("[query]", query)).json()["docs"]

        return resp