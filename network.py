import socket

import settings


class Network():
    def __init__(self, ipAddress):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ipAddress
        self.port = settings.SERVER_PORT
        self.addr = (self.host, self.port)
        self.client.connect(self.addr)
