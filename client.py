import pygame
from network import Network


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
        try:  # "0:(0,0);(click=0);(currentOption=none);(correctOption=none);(nickname=asd)",
            pId = data.split(":")[0]
            coordsData = data.split(":")[1].split(";")[0]
            x = coordsData.split(",")[0].split("(")[1]
            y = coordsData.split(",")[1].split(")")[0]
            click = data.split(":")[1].split(";")[1].split("=")[1].split(")")[0]
            currentOption = data.split(":")[1].split(";")[2].split("=")[1].split(")")[0]
            correctOption = data.split(":")[1].split(";")[3].split("=")[1].split(")")[0]
            nickname = data.split(":")[1].split(";")[4].split("=")[1].split(")")[0]
            return pId, int(x), int(y), int(click), currentOption, correctOption, nickname
        except:
            return "-1", 0, 0, 0, "none", "none", "none"

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
        self.game.window.fill((255, 255, 255))
        bg_img = pygame.image.load(f"assets/continents/{self.game.currentMap}")
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.game.window.blit(bg_img, (20, 20), )

        self.game.currentOption = self.game.getRandomOption()
        self.game.displayOptionData()
        self.game.displayCurrentGameTitle()
        self.game.displayTimeLeft()

        runing = True

        while runing:
            self.game.displayOptionData()
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

            # initTreePixels()
            # writeCountryPixelsInFile("Test", pos[0], pos[1])
            if self.game.player0.id == self.playerId:
                data = f"{self.game.player0.id}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click});(currentOption={self.game.player0.currentOption});(correctOption={self.game.player0.lastCorrectOption});(nickname={self.game.player0.nickname})"
            else:
                data = f"{self.game.player1.id}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click});(currentOption={self.game.player1.currentOption});(correctOption={self.game.player1.lastCorrectOption});(nickname={self.game.player1.nickname})"
            self.network.client.send(str.encode(data))
            reply = self.network.client.recv(2048).decode()

            pId, xData, yData, clickData, currentOption, correctOption, nickname = self.extractData(reply)
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
                data = f"{self.game.player0.id}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click});(currentOption={self.game.player0.currentOption});(correctOption={self.game.player0.lastCorrectOption});(nickname={self.game.player0.nickname})"
            else:
                data = f"{self.game.player1.id}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click});(currentOption={self.game.player1.currentOption});(correctOption={self.game.player1.lastCorrectOption});(nickname={self.game.player1.nickname})"
            self.network.client.send(str.encode(data))
            reply = self.network.client.recv(2048).decode()

            pygame.display.update()
        pygame.quit()
