__author__ = 'Tommy'
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from telegram.bot.tglogging.TGLogger import logger


class HTTPRequestController:
    def __init__(self, url=None, values=None):
        self.url = url
        self.values = values

    def requestwithvaluesxwwwurlencoded(self, url, values):
        data = urlencode(values)
        data = data.encode("ISO-8859-1")

        request = Request(url)
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        response = urlopen(request.get_full_url(), data)
        html = response.read()
        return html

    def requestwithvaluesmultipart(self,url,values):
        data = urlencode(values)
        data = data.encode("utf-8")

        request = Request(url)
        request.add_header("Content-Type","multipart/form-data")
        response = urlopen(request.get_full_url(), data)
        html = response.read()
        return html
