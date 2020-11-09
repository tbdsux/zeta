from dashboard.utils.finder import Finder
import requests


class AsianDrama(Finder):
    def search_asian(self, query):
        # search and get the response
        resp = requests.get(self.kuryana + query).json()["results"]

        print(resp)

        return resp