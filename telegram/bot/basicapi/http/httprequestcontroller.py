__author__ = 'Tommy'
from urllib.request import Request, urlopen
from urllib.parse import urlencode


class HTTPRequestController:
    def __init__(self, url=None, values=None):
        self.url = url
        self.values = values

    def requestWithValues(self, url, values):
        data = urlencode(values)
        data = data.encode("utf-8")

        request = Request(url)
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        response = urlopen(request.get_full_url(), data)
        html = response.read()
        return html
