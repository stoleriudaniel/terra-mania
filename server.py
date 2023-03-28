import socket
from _thread import *

class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIp = socket.gethostbyname('192.168.100.18')
        self.port = 5555
        self.maximumPlayers = 2
        self.currentId = "0"
        self.state = ["0:(0,0);(click=0)", "1:(0,0);(click=0)"]
        self.test = 0

    def create(self):
        try:
            self.sock.bind((self.serverIp, self.port))

        except socket.error as e:
            print(str(e))

        self.sock.listen(self.maximumPlayers)
        print("Waiting for a connection")

        while True:
            conn, addr = self.sock.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))

    def threaded_client(self, conn):
        conn.send(str.encode(self.currentId))
        self.currentId = "1"
        reply = ''
        while True:
            try:
                data = conn.recv(2048)
                reply = data.decode('utf-8')
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    arr = reply.split(":")
                    id = int(arr[0])
                    self.state[id] = reply
                    if ((self.state[0]).find("click=1") or (self.state[1]).find("click=1")) or self.test <= 9:
                        print("test: ", self.test, " reply: ", reply)
                        print("test: ", self.test, " state:", self.state)
                        self.test = self.test + 1
                    opponentId = 0
                    if id == 0: opponentId = 1
                    if id == 1: opponentId = 0

                    reply = self.state[opponentId][:]
                conn.sendall(str.encode(reply))
            except:
                break

        print("Connection Closed")
        conn.close()

Server().create()