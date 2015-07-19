from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import ssl
import os
import sys
import json
from multiprocessing import freeze_support, Process
from telegram.bot.weareone.common.weareonetgbot import WeAreOneBot
from telegram.bot.config.tgbotconfigparser import TGBotConfigParser
from telegram.bot.tglogging.TGLogger import logger

config = TGBotConfigParser()
conf = config.load()


class ForkingHTTPServer(socketserver.ForkingMixIn, HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(10)
        HTTPServer.finish_request(self, request, client_address)
        logger.debug("Request garbaged.")


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        varLen = int(self.headers['content-length'])
        postvar = self.rfile.read(varLen)
        sentMessage = postvar.decode("UTF-8")
        data = json.loads(sentMessage)
        WeAreOneBot.activateBot(data)
        logger.info(
            "Message from @" + str(data["message"]["from"]["username"]) + " with ID #" + str(data["message"]["message_id"]))
        self.handle()


def serve_forever(server):
    logger.info('Starting server.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def start(serveraddr, number_of_processes):
    try:
        srvr = ForkingHTTPServer(serveraddr, RequestHandler)
        logger.info("Server initialised.")

        srvr.socket = ssl.wrap_socket(srvr.socket, keyfile=conf.get("ssl", "keyfile"),
                                      certfile=conf.get("ssl", "certfile"),
                                      ca_certs=conf.get("ssl", "ca_certs"),
                                      server_side=True)
        logger.info("SSL Data inserted.")
        for i in range(number_of_processes - 1):
            Process(target=serve_forever, args=(srvr,)).start()

        serve_forever(srvr)  # serve_forever

    except KeyboardInterrupt:
        logger.info("Server will shut down...")
        srvr.socket.close()


def start_pipe():
    DIR = os.path.join(os.path.dirname(__file__), '..')
    serveraddr = (conf.get("basics", "address"), int(conf.get("basics", "port")))
    processes = 10

    logger.info('Serving at http://%s:%d using %d worker processes' % \
                (serveraddr[0], serveraddr[1], processes))

    os.chdir(DIR)
    start(serveraddr, processes)


if __name__ == '__main__':
    freeze_support()
    start_pipe()
