from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import ssl
import json
from telegram.bot.weareone.common.weareonetgbot import WeAreOneBot
from telegram.bot.config.tgbotconfigparser import TGBotConfigParser

config = TGBotConfigParser("config.ini")
conf = config.load()


class ForkingHTTPServer(socketserver.ForkingMixIn, HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(30)
        # "super" can not be used because BaseServer is not created from object
        HTTPServer.finish_request(self, request, client_address)


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        varLen = int(self.headers['content-length'])
        postvar = self.rfile.read(varLen)
        sentMessage = postvar.decode("UTF-8")
        data = json.loads(sentMessage)
        print(data["message"]["from"])
        WeAreOneBot.activateBot(data)
        return None


def start():
    try:
        serveraddr = (conf.get("basics", "address"), int(conf.get("basics", "port")))
        srvr = ForkingHTTPServer(serveraddr, RequestHandler)
        srvr.socket = ssl.wrap_socket(srvr.socket, keyfile=conf.get("ssl", "keyfile"),
                                      certfile=conf.get("ssl", "certfile"),
                                      ca_certs=conf.get("ssl", "ca_certs"),
                                      server_side=True)
        srvr.serve_forever()  # serve_forever
    except KeyboardInterrupt:
        srvr.socket.close()


if __name__ == '__main__':
    start()
