import socket

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.100.4"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.client.connect(self.addr)