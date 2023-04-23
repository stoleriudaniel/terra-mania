import psutil
import pygame
from network import Network
from button import Button

class Client:
    def __init__(self, gameParam, ipAddress, nickname):
        self.game = gameParam
        self.network = Network(ipAddress)
        self.playerId, self.game.gameType, self.game.indexMapAndContinent = self.getInitDataFromServer()
        self.game.CONTINENT = self.game.continents[self.game.indexMapAndContinent]
        self.game.currentMap = self.game.maps[self.game.indexMapAndContinent]
        self.clickPlayer0 = 0
        self.clickPlayer1 = 0
        self.initNickname(nickname)
        self.start = False
        self.stopServer = False
        self.gameStatus = None

    def initNickname(self, nickname):
        if self.playerId == "0":
            self.game.player0.nickname = nickname
        elif self.playerId == "1":
            self.game.player1.nickname = nickname

    def getInitDataFromServer(self):
        data = self.network.client.recv(2048).decode()
        try:
            pId = data.split(":")[0]
            gameType = data.split(":")[1].split(";")[0].split("=")[1].split(")")[0]
            strIndexMapAndContinent = data.split(":")[1].split(";")[1].split("=")[1].split(")")[0]
            return pId, gameType, int(strIndexMapAndContinent)
        except:
            return "-1", "none", 0

    def extractData(self, data):
        try:  # "0:(0,0);(click=0);(currentOption=none);(correctOption=none);(nickname=asd);(status=play)",
            pId = data.split(":")[0]
            coordsData = data.split(":")[1].split(";")[0]
            x = coordsData.split(",")[0].split("(")[1]
            y = coordsData.split(",")[1].split(")")[0]
            click = data.split(":")[1].split(";")[1].split("=")[1].split(")")[0]
            currentOption = data.split(":")[1].split(";")[2].split("=")[1].split(")")[0]
            correctOption = data.split(":")[1].split(";")[3].split("=")[1].split(")")[0]
            nickname = data.split(":")[1].split(";")[4].split("=")[1].split(")")[0]
            status = data.split(":")[1].split(";")[5].split("=")[1].split(")")[0]
            gameTime = data.split("%")[1].split("=")[1].split(")")[0]
            return pId, int(x), int(y), int(click), currentOption, correctOption, nickname, status, gameTime
        except:
            return "-1", 0, 0, 0, "none", "none", "", "play", "none"

    def initGame(self):
        self.game.window.fill((255, 255, 255))
        bg_img = pygame.image.load(f"assets/continents/{self.game.currentMap}")
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.game.window.blit(bg_img, (20, 20), )

        self.game.currentOption = self.game.getRandomOption()
        self.game.displayOptionData()
        self.game.displayCurrentGameTitle()
        self.game.displayTimeLeft()

    def waitingForTheSecondPlayer(self):
        self.game.window.fill((255, 255, 255))
        bg_img = pygame.image.load(f"assets/menu/8.jpg")
        bg_img = pygame.transform.scale(bg_img, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))

        while self.start is False:
            self.game.window.blit(bg_img, (0, 0), )
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT1 = self.game.get_font(30).render("Waiting for the second", True, "#d7fcd4")
            MENU_RECT1 = MENU_TEXT1.get_rect(center=(640, 230))
            self.game.window.blit(MENU_TEXT1, MENU_RECT1)
            MENU_TEXT = self.game.get_font(30).render("player to connect...", True, "#d7fcd4")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 270))
            self.game.window.blit(MENU_TEXT, MENU_RECT)
            STOP_SERVER_BUTTON = Button(image=None, pos=(650, 532),
                                  text_input="Stop Server", font=self.game.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [STOP_SERVER_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.game.window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if STOP_SERVER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.stopServer = True
                        return

            self.getDataFromServer()

            if self.game.player0.nickname != "" and self.game.player1.nickname != "":
                if self.start is False:
                    self.initGame()
                    self.start = True

            pygame.display.update()

    def serverClosed(self):
        self.game.window.fill((255, 255, 255))
        bg_img = pygame.image.load(f"assets/menu/8.jpg")
        bg_img = pygame.transform.scale(bg_img, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
        betterPlayer = ""
        win = ""
        if len(self.game.player0.correctOptions) <= 0 and len(self.game.player1.correctOptions) <= 0:
            betterPlayer = ""
        elif len(self.game.player0.correctOptions) > len(self.game.player1.correctOptions):
            betterPlayer = self.game.player0.nickname
        elif len(self.game.player0.correctOptions) < len(self.game.player1.correctOptions):
            betterPlayer = self.game.player1.nickname

        if betterPlayer != "":
            win = f"Win: {betterPlayer}"
        while True:
            self.game.window.blit(bg_img, (0, 0), )
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.game.get_font(40).render("Game is ended.", True, "#d7fcd4")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 220))
            self.game.window.blit(MENU_TEXT, MENU_RECT)

            player0text = f"{self.game.player0.nickname} score: {len(self.game.player0.correctOptions)}"
            player1text = f"{self.game.player1.nickname} score: {len(self.game.player1.correctOptions)}"

            PLAYER0_TEXT = self.game.get_font(25).render(player0text, True, "#d7fcd4")
            PLAYER0_RECT = PLAYER0_TEXT.get_rect(center=(640, 290))
            self.game.window.blit(PLAYER0_TEXT, PLAYER0_RECT)

            PLAYER1_TEXT = self.game.get_font(25).render(player1text, True, "#d7fcd4")
            PLAYER1_RECT = PLAYER1_TEXT.get_rect(center=(640, 340))
            self.game.window.blit(PLAYER1_TEXT, PLAYER1_RECT)

            WIN_TEXT = self.game.get_font(25).render(win, True, "Green")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 390))
            self.game.window.blit(WIN_TEXT, WIN_RECT)

            BACK_BUTTON = Button(image=None, pos=(640, 532),
                                  text_input="Back", font=self.game.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.game.window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        return True

            pygame.display.update()

    def killProcessByPort(self, port):
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and conn.laddr.port == port:
                pid = conn.pid
                process = psutil.Process(pid)
                process.kill()
                print(f"Killed process {pid} listening on port {port}")
                return
        print(f"No process found listening on port {port}")

    def getDataFromServer(self):
        if self.game.player0.id == self.playerId:
            data = f"{self.game.player0.id}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click});(currentOption={self.game.player0.currentOption});(correctOption={self.game.player0.lastCorrectOption});(nickname={self.game.player0.nickname});(status={self.gameStatus});(gameTime={self.game.gameTime})"
        else:
            data = f"{self.game.player1.id}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click});(currentOption={self.game.player1.currentOption});(correctOption={self.game.player1.lastCorrectOption});(nickname={self.game.player1.nickname});(status={self.gameStatus});(gameTime={self.game.gameTime})"
        self.network.client.send(str.encode(data))
        reply = self.network.client.recv(2048).decode()

        pId, xData, yData, clickData, currentOption, correctOption, nickname, status, gameTime = self.extractData(reply)
        self.game.gameTime = gameTime
        if pId == self.game.player0.id:
            self.game.player0.x, self.game.player0.y, self.game.player0.click, self.game.player0.nickname = xData, yData, clickData, nickname
            if currentOption != "none":
                self.game.player0.currentOption = currentOption
            if correctOption != "none":
                self.game.player0.lastCorrectOption = correctOption
                if correctOption not in self.game.player0.correctOptions:
                    self.game.player0.correctOptions.append(correctOption)
        elif pId == self.game.player1.id:
            self.game.player1.x, self.game.player1.y, self.game.player1.click, self.game.player1.nickname = xData, yData, clickData, nickname
            if currentOption != "none":
                self.game.player1.currentOption = currentOption
            if correctOption != "none":
                self.game.player1.lastCorrectOption = correctOption
                if correctOption not in self.game.player1.correctOptions:
                    self.game.player1.correctOptions.append(correctOption)
        # Render the coordinates text
        if self.game.player0.id == self.playerId:
            data = f"{self.game.player0.id}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click});(currentOption={self.game.player0.currentOption});(correctOption={self.game.player0.lastCorrectOption});(nickname={self.game.player0.nickname});(status={self.gameStatus});(gameTime={self.game.gameTime})"
        else:
            data = f"{self.game.player1.id}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click});(currentOption={self.game.player1.currentOption});(correctOption={self.game.player1.lastCorrectOption});(nickname={self.game.player1.nickname});(status={self.gameStatus});(gameTime={self.game.gameTime})"
        self.network.client.send(str.encode(data))
        reply = self.network.client.recv(2048).decode()

    def play(self):
        pygame.init()
        pygame.display.set_caption("Menu")
        self.game.playerId = self.playerId
        self.game.player0.currentOption = self.game.getOptionByIndex(0)
        self.game.player1.currentOption = self.game.getOptionByIndex(1)
        yellow = (238, 224, 29)
        green = (23, 165, 23)
        blue1 = (0, 51, 153)
        self.game.isMultiplayer = True

        runing = True

        QUIT_BUTTON = Button(image=None, pos=(1190, 655),
                             text_input="Quit", font=self.game.get_font(30), base_color="Red",
                             hovering_color="Blue")

        while runing:
            try:
                if self.start is True:
                    self.game.displayOptionData()
                    self.game.displayTimeLeft()

                    MENU_MOUSE_POS = pygame.mouse.get_pos()
                    for button in [QUIT_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(self.game.window)

                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.MOUSEMOTION:  # MOUSEBUTTONUP MOUSEMOTION
                            pos = pygame.mouse.get_pos()
                            if self.playerId == self.game.player0.id:
                                self.game.player0.x = pos[0]
                                self.game.player0.y = pos[1]
                            else:
                                self.game.player1.x = pos[0]
                                self.game.player1.y = pos[1]
                        if event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            if QUIT_BUTTON.checkForInput((pos[0], pos[1])):
                                self.gameStatus = "quit"
                            self.game.changeOptionIfArrowClicked(pos[0], pos[1])
                            self.game.displayOptionData()
                            self.game.drawCorrectCountry(pos[0], pos[1], yellow, green, self.playerId)
                            if self.playerId == self.game.player0.id:
                                self.game.player0.click = 1 - self.game.player0.click
                            elif self.playerId == self.game.player1.id:
                                self.game.player1.click = 1 - self.game.player1.click
                    if self.playerId != self.game.player0.id and self.game.player0.click != self.clickPlayer0:
                        self.game.drawCorrectCountry(self.game.player0.x, self.game.player0.y, yellow, green,
                                                     self.game.player0.id)
                        self.clickPlayer0 = self.game.player0.click
                    elif self.playerId != self.game.player1.id and self.game.player1.click != self.clickPlayer1:
                        self.game.drawCorrectCountry(self.game.player1.x, self.game.player1.y, yellow, green,
                                                     self.game.player1.id)
                        self.clickPlayer1 = self.game.player1.click
                    self.game.undrawCountries(blue1)
                    self.game.drawCountry(self.game.player0.x, self.game.player0.y, blue1, yellow, self.game.player0.id)
                    self.game.drawCountry(self.game.player1.x, self.game.player1.y, blue1, yellow, self.game.player1.id)
                if self.start is False:
                    self.waitingForTheSecondPlayer()
                    if self.stopServer is True:
                        self.killProcessByPort(5556)
                        return
                self.getDataFromServer()

                pygame.display.update()
            except:
                if self.serverClosed():
                    return

        pygame.quit()
