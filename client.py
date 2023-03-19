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
        self.click = 0

    def extractData(self, data):
        try:
            coordsData = data.split(":")[1].split(";")[0]
            x = coordsData.split(",")[0].split("(")[1]
            y = coordsData.split(",")[1].split(")")[0]
            click = data.split(":")[1].split(";")[1].split("=")[1].split(")")[0]
            return int(x), int(y), int(click)
        except:
            return 0, 0, 0

    def play(self):
        pygame.init()
        pygame.display.set_caption("Menu")
        # hand = HandTrackingModule.HandDetector()
        # hand.show()
        yellow = (238, 224, 29)
        green = (23, 165, 23)
        blue1 = (0, 51, 153)
        self.game.window.fill((255, 255, 255))
        bg_img = pygame.image.load(self.game.currentMap)
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.game.window.blit(bg_img, (20, 20), )

        self.game.currentOption = self.game.getRandomOption()
        self.game.displayOption()
        arrow_right = pygame.image.load("arrow_right.png")
        arrow_right = pygame.transform.scale(arrow_right, (80, 65))
        self.game.window.blit(arrow_right, (1170, 215))

        arrow_left = pygame.image.load("arrow_left.png")
        arrow_left = pygame.transform.scale(arrow_left, (80, 65))
        self.game.window.blit(arrow_left, (920, 215))

        arrowColor = (34, 177, 76)
        runing = True

        font = pygame.font.SysFont(None, 48)  # choose font and font size
        print("hellooo22")
        while runing:
            print(f"({self.game.player0.x},{self.game.player0.y}); ({self.game.player1.x},{self.game.player1.y})")
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEMOTION:  # MOUSEBUTTONUP MOUSEMOTION
                    pos = pygame.mouse.get_pos()

                    self.game.player0.x = pos[0]
                    self.game.player0.y = pos[1]

                    self.game.player1.x = pos[0]
                    self.game.player1.x = pos[1]

            self.game.undrawCountries(blue1)
            self.game.drawCountry(self.game.player0.x, self.game.player0.y, blue1, yellow)
            self.game.drawCountry(self.game.player1.x, self.game.player1.y, blue1, yellow)
                # if event.type == pygame.MOUSEBUTTONUP:
                #     pos = pygame.mouse.get_pos()
                #     self.game.changeOptionIfArrowClicked(pos[0], pos[1])
                #     self.game.displayOption()
                #     self.game.drawCorrectCountry(pos[0], pos[1], yellow, green)

                # initTreePixels()
                # writeCountryPixelsInFile("Test", pos[0], pos[1])

            data = f"{self.playerId}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.click})"
            self.network.client.send(str.encode(data))
            reply = self.network.client.recv(2048).decode()

            self.game.player1.x, self.game.player1.y, self.click = self.extractData(reply)
            # Fill the screen with white
            # self.game.window.fill((255, 255, 255))

            # Render the coordinates text
            data = f"{self.playerId}:({str(self.game.player0.x)},{str(self.game.player0.y)});(click={self.click})"
            self.network.client.send(str.encode(data))
            reply = self.network.client.recv(2048).decode()

            # text1 = font.render(f"Mouse coordinates player1: {self.player0.x}, {self.player0.y}", True, (0, 0, 0))
            # self.game.window.blit(text1, (10, 10))
            # text2 = font.render(f"Mouse coordinates player2: {self.player1.x}, {self.player1.y}", True, (0, 0, 0))
            # self.game.window.blit(text2, (10, 60))

            pygame.display.update()
        pygame.quit()
