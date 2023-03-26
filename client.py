import socket
import pygame
from player import Player
from network import Network
from game import Game


class Client():
    def __init__(self):
        self.game = Game()
        self.network = Network()
        self.playerId = self.network.client.recv(2048).decode()
        self.test = 0

    def extractData(self, data):
        try:
            # print(data)
            pId = data.split(":")[0]
            coordsData = data.split(":")[1].split(";")[0]
            x = coordsData.split(",")[0].split("(")[1]
            y = coordsData.split(",")[1].split(")")[0]
            click = data.split(":")[1].split(";")[1].split("=")[1].split(")")[0]
            return pId, int(x), int(y), int(click)
        except:
            return "0", 0, 0, 0

    def play(self):
        pygame.init()
        pygame.display.set_caption("Menu")
        # hand = HandTrackingModule.HandDetector()
        # hand.show()
        self.game.playerId = self.playerId
        # self.game.player0.id = self.playerId
        # self.game.player1.id = str(1 - int(self.playerId))
        self.game.player0.currentOption = self.game.getRandomOption()
        self.game.player1.currentOption = self.game.getRandomOption()
        yellow = (238, 224, 29)
        green = (23, 165, 23)
        blue1 = (0, 51, 153)
        self.game.isMultiplayer = True
        self.game.window.fill((255, 255, 255))
        bg_img = pygame.image.load(self.game.currentMap)
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.game.window.blit(bg_img, (20, 20), )

        self.game.currentOption = self.game.getRandomOption()
        self.game.displayOptionData()
        self.game.displayCurrentGameTitle()
        self.game.displayTimeLeft()
        # arrow_right = pygame.image.load("arrow_right.png")
        # arrow_right = pygame.transform.scale(arrow_right, (80, 65))
        # self.game.window.blit(arrow_right, (1170, 215))
        #
        # arrow_left = pygame.image.load("arrow_left.png")
        # arrow_left = pygame.transform.scale(arrow_left, (80, 65))
        # self.game.window.blit(arrow_left, (920, 215))

        arrowColor = (34, 177, 76)
        runing = True

        font = pygame.font.SysFont(None, 48)  # choose font and font size
        print("hellooo22")
        while runing:
            # print("player0 id:", self.game.player0.id)
            # print("player1 id:", self.game.player1.id)
            # print(f"({self.game.player0.x},{self.game.player0.y}); ({self.game.player1.x},{self.game.player1.y})")
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
                        self.game.player0.click = 1
                    elif self.playerId == self.game.player1.id:
                        self.game.player1.click = 1
            if self.game.player0.click == 1 or self.game.player1.click == 1:
                print(f"{self.game.player0.id}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click})")
                print(f"{self.game.player1.id}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click})")
                if self.game.player0.click == 1:
                    self.game.drawCorrectCountry(self.game.player0.x, self.game.player0.y, yellow, green, self.game.player0.id)
                if self.game.player1.click == 1:
                    self.game.drawCorrectCountry(self.game.player1.x, self.game.player1.y, yellow, green, self.game.player1.id)
            self.game.undrawCountries(blue1)
            self.game.drawCountry(self.game.player0.x, self.game.player0.y, blue1, yellow, self.game.player0.id)
            self.game.drawCountry(self.game.player1.x, self.game.player1.y, blue1, yellow, self.game.player1.id)
            # if event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     self.game.changeOptionIfArrowClicked(pos[0], pos[1])
            #     self.game.displayOption()
            #     self.game.drawCorrectCountry(pos[0], pos[1], yellow, green)

            # initTreePixels()
            # writeCountryPixelsInFile("Test", pos[0], pos[1])

            if self.game.player0.id == self.playerId:
                data = f"{self.game.player0.id}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click})"
            else:
                data = f"{self.game.player1.id}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click})"
            self.network.client.send(str.encode(data))
            reply = self.network.client.recv(2048).decode()

            pId, xData, yData, clickData = self.extractData(reply)
            if self.playerId != self.game.player0.id:
                self.game.player0.x, self.game.player0.y, self.game.player0.click = xData, yData, clickData
            else:
                self.game.player1.x, self.game.player1.y, self.game.player1.click = xData, yData, clickData
            # Fill the screen with white
            # self.game.window.fill((255, 255, 255))

            # Render the coordinates text
            if self.game.player0.id == self.playerId:
                data = f"{self.playerId}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.game.player0.click})"
            else:
                data = f"{self.playerId}:({str(self.game.player1.x)},{str(self.game.player1.y)});(click={self.game.player1.click})"
            self.network.client.send(str.encode(data))
            reply = self.network.client.recv(2048).decode()

            # text1 = font.render(f"{self.game.player0.id}: {self.game.player0.x},{self.game.player0.y}", True, (0, 0, 0))
            # self.game.window.blit(text1, (10, 10))
            # text2 = font.render(f"{self.game.player1.id}: {self.game.player1.x},{self.game.player1.y}", True, (0, 0, 0))
            # self.game.window.blit(text2, (10, 60))

            pygame.display.update()
        pygame.quit()