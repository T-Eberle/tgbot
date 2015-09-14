__author__ = 'Thomas Eberle'

from telegram.basicapi.http.httprequestcontroller import HTTPRequestController
from telegram.config.tgbotconfigparser import TGBotConfigParser
from requests.exceptions import HTTPError

config = TGBotConfigParser("config.ini")
data = config.load()


def dosomething(method_name,oldvalues,**kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = data.get("tgapi", "bot_link") + data.get("tgapi", method_name + "_Method")
    values["parse_mode"] = "Markdown"
    try:
        HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)
    except HTTPError:
        del values["parse_mode"]
        HTTPRequestController.requestwithvaluesxwwwurlencoded(url, values)


def dosomethingwithfile(method_name,file_id,filename,oldvalues={},path="resources.documents",complete_path=None,
                        **kwargs):
    values = oldvalues
    for key in kwargs:
        values[str(key)] = kwargs[key]
    url = data.get("tgapi", "bot_link") + data.get("tgapi", method_name + "_Method")
    values["parse_mode"] = "Markdown"
    HTTPRequestController.requestwithdoc(url,values,file_id,filename,path=path,complete_path=complete_path)
