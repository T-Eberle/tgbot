__author__ = 'Tommy'
from urllib.request import Request, urlopen
from urllib.parse import urlencode


class HTTPRequestController:
    def __init__(self,url=None,values=None):
        self.url = url
        self.values = values

    def requestWithValues(self, url, values):
        data = urlencode(values)
        binary_data = data.encode("utf-8")
        request = Request(url, binary_data)
        response = urlopen(request.get_full_url(),request.data)
        html = response.read()
        return html

