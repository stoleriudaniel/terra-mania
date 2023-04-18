import socket


class Network():
    def __init__(self, ipAddress):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ipAddress
        self.port = 5556
        self.addr = (self.host, self.port)
        self.client.connect(self.addr)
