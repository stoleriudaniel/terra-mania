import socket
from _thread import *
import time

import psutil


class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIp = socket.gethostbyname('localhost')
        self.port = 5556
        self.maximumPlayers = 2
        self.currentId = "0"
        self.gameType = ""
        self.indexMapAndContinent = 0
        self.gameTime = ""
        self.state = [f"0:(0,0);(click=0);(currentOption=none);(correctOption=none);(nickname=);(status=none)%(gameTime={self.gameTime})",
                      f"1:(0,0);(click=0);(currentOption=none);(correctOption=none);(nickname=);(status=none)%(gameTime={self.gameTime})"]
        self.timeStarted = False
        self.t = 120

    def bothPlayersConnected(self):
        nickname0 = self.state[0].split(":")[1].split(";")[4].split("=")[1].split(")")[0]
        nickname1 = self.state[1].split(":")[1].split(";")[4].split("=")[1].split(")")[0]
        if nickname0 != "" and nickname1 != "":
            return True
        return False

    def countdown(self):
        while self.t:
            mins, secs = divmod(self.t, 60)
            self.gameTime = '{:02d}:{:02d}'.format(mins, secs)
            print(self.gameTime, end="\r")
            time.sleep(1)
            self.t -= 1

    def replaceTime(self):
        arrSplited = self.state[0].split("%")
        self.state[0] = f"{arrSplited[0]}%(gameTime={self.gameTime})"
        arrSplited = self.state[1].split("%")
        self.state[1] = f"{arrSplited[0]}%(gameTime={self.gameTime})"

    def playerQuit(self):
        statusPlayer0 = self.state[0].split(":")[1].split(";")[5].split("=")[1].split(")")[0]
        statusPlayer1 = self.state[1].split(":")[1].split(";")[5].split("=")[1].split(")")[0]
        if "quit" in [statusPlayer0, statusPlayer1]:
            return True
        return False

    def create(self, ipAddress, gameType, strIndexMapAndContinent):
        self.gameType = gameType
        self.indexMapAndContinent = int(strIndexMapAndContinent)
        self.state[0] = self.state[0].replace("gameType=none", f"gameType={gameType}")
        self.state[0] = self.state[0].replace("indexMapAndContinent=none",
                                              f"indexMapAndContinent={strIndexMapAndContinent}")
        self.state[1] = self.state[1].replace("gameType=none", f"gameType={gameType}")
        self.state[1] = self.state[1].replace("indexMapAndContinent=none",
                                              f"indexMapAndContinent={strIndexMapAndContinent}")
        self.serverIp = socket.gethostbyname(ipAddress)
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
        conn.send(str.encode(
            f"{self.currentId}:(gameType={self.gameType});(indexMapAndContinent={str(self.indexMapAndContinent)})"))
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
                    if self.timeStarted is False:
                        if self.bothPlayersConnected():
                            self.timeStarted = True
                            start_new_thread(self.countdown, ())
                    arr = reply.split(":")
                    id = int(arr[0])
                    self.state[id] = reply
                    self.replaceTime()
                    if self.playerQuit():
                        self.killProcessByPort()
                    opponentId = 0
                    if id == 0: opponentId = 1
                    if id == 1: opponentId = 0

                    reply = self.state[opponentId][:]
                conn.sendall(str.encode(reply))
            except:
                break

        print("Connection Closed")
        conn.close()

    def killProcessByPort(self):
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and conn.laddr.port == self.port:
                pid = conn.pid
                process = psutil.Process(pid)
                process.kill()
                print(f"Killed process {pid} listening on port {self.port}")
                return
        print(f"No process found listening on port {self.port}")

# Server().create()
