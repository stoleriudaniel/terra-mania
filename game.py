import threading
import cv2.data
import HandTrackingModule
from network import Network
import os
import random
from pathlib import Path

import pygame
import sys
from player import Player
from button import Button


class Game:

    def __init__(self):
        self.playerId = 0
        self.player0 = Player(0, 0, "0")
        self.player1 = Player(0, 0, "1")
        self.isMultiplayer = False
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.BG = pygame.image.load("assets/Background.png")
        # self.net = Network()
        self.maps = ['Europe_map1.png', 'south_america112.png', 'north-america111.png', 'asia1.png', 'africa111.png',
                     'oceania111.png']
        self.continents = ["Europe", "South-America", "North-America", "Asia", "Africa", "Oceania"]
        self.CONTINENT = self.continents[3]
        self.currentMap = self.maps[3]

        self.language = "Romanian"

        self.gameTypeFlags = "flags"
        self.gameTypeCapitals = "capitals"
        self.gameTypeCountries = "countries"

        self.gameType = self.gameTypeCountries

        self.hoverColoredCountries = []

        self.correctCountries = []
        self.correctFlags = []
        self.correctCapitals = []

        self.correctOptions = []

        self.incorrectCountries = []

        self.currentOption = ""
        self.currentHoveredCountry = ""

        self.mapRealWidth = 0
        self.mapRealHeight = 0

        self.computerVision = False

        self.cvx = 0
        self.cvy = 0

    def initTreePixelsArrows(self):
        print("In initTreePixels")
        # directories = [x[0] for x in os.walk(f"countries\\{self.CONTINENT}")]
        directories = [x[0] for x in os.walk(f"arrows")]
        countries = []
        print(directories)
        for index in range(0, len(directories)):
            country = directories[index].split("\\")
            if len(country) > 1:
                # path = Path(f"countries\\{self.CONTINENT}\\{country[2]}\\pixels.txt")
                path = Path(f"arrows\\{country[1]}\\pixels.txt")
                if not path.is_file():
                    continue
                print("country: ", country[1])
                # pixelsFile = open(f"countries\\{self.CONTINENT}\\{country[2]}\\pixels.txt", "r")
                pixelsFile = open(f"arrows\\{country[1]}\\pixels.txt", "r")
                rows = pixelsFile.readlines()
                for row in rows:
                    result = row.split()
                    xCord = result[0]
                    yCord = result[1]
                    filename = int(xCord) // 100 * 100
                    # file = open(f"tree\\countries\\{self.CONTINENT}\\pixels\\{filename}.txt", "a")
                    file = open(f"tree\\others\\pixels\\{filename}.txt", "a")
                    file.write(f"{xCord} {yCord} {country[1]}\n")
        print("Finish")

    def initTreePixels(self):
        print("In initTreePixels")
        directories = [x[0] for x in os.walk(f"countries\\{self.CONTINENT}")]
        countries = []
        for index in range(0, len(directories)):
            country = directories[index].split("\\")
            if len(country) > 2:
                path = Path(f"countries\\{self.CONTINENT}\\{country[2]}\\pixels.txt")
                if not path.is_file():
                    continue
                print("country: ", country[2])
                pixelsFile = open(f"countries\\{self.CONTINENT}\\{country[2]}\\pixels.txt", "r")
                rows = pixelsFile.readlines()
                for row in rows:
                    result = row.split()
                    xCord = result[0]
                    yCord = result[1]
                    filename = int(xCord) // 100 * 100
                    file = open(f"tree\\countries\\{self.CONTINENT}\\pixels\\{filename}.txt", "a")
                    file.write(f"{xCord} {yCord} {country[2]}\n")
        print("Finish")

    def writeCountryPixelsInFile(self, countryName, mousex, mousey):
        file = open(f"arrows\\{countryName}\\pixels.txt", "w")
        # file = open(f"arrows\\{countryName}\\pixels.txt", "w")
        margin = (0, 0, 0)  # black
        uncolored = (0, 51, 153)  # blue
        newColor = (238, 224, 29)  # yellow
        arrowColor = (34, 177, 76)
        uncolored = arrowColor
        finished = False
        uncoloredPixelsList = []
        c = self.window.get_at((mousex, mousey))
        if (c[0], c[1], c[2]) == uncolored:
            uncoloredPixelsList.append((mousex, mousey))
        while uncoloredPixelsList:
            currentPixel = uncoloredPixelsList.pop(0)
            file.write(f"{currentPixel[0]} {currentPixel[1]}\n")
            self.window.set_at((currentPixel[0], currentPixel[1]), newColor)
            c1 = self.window.get_at((currentPixel[0] - 1, currentPixel[1] + 1))
            c2 = self.window.get_at((currentPixel[0], currentPixel[1] + 1))
            c3 = self.window.get_at((currentPixel[0] + 1, currentPixel[1] + 1))
            c4 = self.window.get_at((currentPixel[0] + 1, currentPixel[1]))
            c5 = self.window.get_at((currentPixel[0] + 1, currentPixel[1] - 1))
            c6 = self.window.get_at((currentPixel[0], currentPixel[1] - 1))
            c7 = self.window.get_at((currentPixel[0] - 1, currentPixel[1] - 1))
            c8 = self.window.get_at((currentPixel[0] - 1, currentPixel[1]))
            if (c1[0], c1[1], c1[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0] - 1, currentPixel[1] + 1))
            if (c2[0], c2[1], c2[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0], currentPixel[1] + 1))
            if (c3[0], c3[1], c3[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0] + 1, currentPixel[1] + 1))
            if (c4[0], c4[1], c4[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0] + 1, currentPixel[1]))
            if (c5[0], c5[1], c5[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0] + 1, currentPixel[1] - 1))
            if (c6[0], c6[1], c6[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0], currentPixel[1] - 1))
            if (c7[0], c7[1], c7[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0] - 1, currentPixel[1] - 1))
            if (c8[0], c8[1], c8[2]) == uncolored:
                uncoloredPixelsList.append((currentPixel[0] - 1, currentPixel[1]))
            uncoloredPixelsList = set(uncoloredPixelsList)
            uncoloredPixelsList = list(uncoloredPixelsList)
        print("Finish")
        file.close()

    def drawCountry(self, mouseX, mouseY, initRgb, newRgb, playerIdParam="0"):
        red = (255, 0, 0)
        country = ""
        c = self.window.get_at((mouseX, mouseY))
        # print((c[0], c[1], c[2]) != initRgb, c)
        if (c[0], c[1], c[2]) != initRgb:
            if (c[0], c[1], c[2]) != red:
                if self.isMultiplayer:
                    if playerIdParam == self.player0.id:
                        self.player0.currentHoveredCountry = country
                    else:
                        self.player1.currentHoveredCountry = country
                else:
                    self.currentHoveredCountry = country
            return
        treeFilename = mouseX // 100 * 100
        treeFile = open(f"tree\\countries\\{self.CONTINENT}\\pixels\\{treeFilename}.txt", "r")
        rows = treeFile.readlines()
        for row in rows:
            result = row.split()
            xCord = result[0]
            yCord = result[1]
            if int(xCord) == mouseX and int(yCord) == mouseY:
                country = result[2]
                break
        if country == "":
            return

        if self.isMultiplayer:
            if playerIdParam == self.player0.id:
                self.player0.currentHoveredCountry = country
                self.drawCountryByCountryParam(country, newRgb)
                self.player0.hoverColoredCountries.append(country)
            else:
                self.player1.currentHoveredCountry = country
                self.drawCountryByCountryParam(country, newRgb)
                self.player1.hoverColoredCountries.append(country)
        else:
            self.currentHoveredCountry = country
            self.drawCountryByCountryParam(country, newRgb)
            self.hoverColoredCountries.append(country)

    def drawCorrectCountry(self, mouseX, mouseY, initRgb, newRgb, playerIdParam="0"):
        # print("playerIdParam: ", playerIdParam)
        c = self.window.get_at((mouseX, mouseY))
        if (c[0], c[1], c[2]) != initRgb:
            return
        country = ""
        treeFilename = mouseX // 100 * 100
        treeFile = open(f"tree\\countries\\{self.CONTINENT}\\pixels\\{treeFilename}.txt", "r")
        rows = treeFile.readlines()
        for row in rows:
            result = row.split()
            xCord = result[0]
            yCord = result[1]
            if int(xCord) == mouseX and int(yCord) == mouseY:
                country = result[2]
                break
        if country == "":
            return
        # print("country: ", country)
        if self.isMultiplayer:
            if self.player0.id == playerIdParam:
                if country == self.player0.currentOption or country == self.player0.lastCorrectOption:
                    # print("call drawCountryByCountryParam rgb self.playerId:", self.playerId, " self.player0.id:", self.player0.id, " playerIdParam:", playerIdParam)
                    self.player0.lastCorrectOption = country
                    self.drawCountryByCountryParam(country, newRgb)
                    self.player0.hoverColoredCountries.remove(country)
                    self.player0.correctOptions.append(country)
                    self.getNextOption()
                else:
                    # print("call else stmt player0")
                    # print("call drawCountryByCountryParam rgb self.playerId:", self.playerId, " self.player0.id:", self.player0.id, " playerIdParam:", playerIdParam)
                    self.player0.incorrectCountries.append(country)
                    red = (255, 0, 0)
                    self.drawCountryByCountryParam(country, red)
                    self.player0.hoverColoredCountries.remove(country)
            elif self.player1.id == playerIdParam:
                if country == self.player1.currentOption or country == self.player1.lastCorrectOption:
                    # print("call drawCountryByCountryParam rgb self.playerId:", self.playerId, " self.player1.id:",self.player1.id, " playerIdParam:", playerIdParam)
                    self.player1.lastCorrectOption = country
                    self.drawCountryByCountryParam(country, newRgb)
                    self.player1.hoverColoredCountries.remove(country)
                    self.player1.correctOptions.append(country)
                    self.getNextOption()
                else:
                    # print("call else stmt player0")
                    # print("call drawCountryByCountryParam rgb self.playerId:", self.playerId, " self.player1.id:", self.player1.id, " playerIdParam:", playerIdParam)
                    self.player1.incorrectCountries.append(country)
                    red = (255, 0, 0)
                    self.drawCountryByCountryParam(country, red)
                    self.player1.hoverColoredCountries.remove(country)
            self.player0.correctOptions = list(dict.fromkeys(self.player0.correctOptions))
            self.player1.correctOptions = list(dict.fromkeys(self.player1.correctOptions))
        else:
            if country == self.currentOption:
                self.drawCountryByCountryParam(country, newRgb)
                self.hoverColoredCountries.remove(country)
                self.correctOptions.append(country)
                self.getNextOption()
            else:
                self.incorrectCountries.append(country)
                red = (255, 0, 0)
                self.drawCountryByCountryParam(country, red)
                self.hoverColoredCountries.remove(country)

    def undrawCountries(self, newRGB):
        # print("before - player0:", self.player0.hoverColoredCountries)
        # print("before - player1:", self.player1.hoverColoredCountries)
        if self.isMultiplayer:
            for incorrectCountry in self.player0.incorrectCountries:
                if incorrectCountry != self.player0.currentHoveredCountry:
                    self.player0.hoverColoredCountries.append(incorrectCountry)
                    self.player0.incorrectCountries.remove(incorrectCountry)
            for country in self.player0.hoverColoredCountries:
                self.drawCountryByCountryParam(country, newRGB)
                self.player0.hoverColoredCountries.remove(country)
            ## player 1
            for incorrectCountry in self.player1.incorrectCountries:
                if incorrectCountry != self.player1.currentHoveredCountry:
                    self.player1.hoverColoredCountries.append(incorrectCountry)
                    self.player1.incorrectCountries.remove(incorrectCountry)
            for country in self.player1.hoverColoredCountries:
                self.drawCountryByCountryParam(country, newRGB)
                self.player1.hoverColoredCountries.remove(country)
        else:
            for incorrectCountry in self.incorrectCountries:
                if incorrectCountry != self.currentHoveredCountry:
                    self.hoverColoredCountries.append(incorrectCountry)
                    self.incorrectCountries.remove(incorrectCountry)
            for country in self.hoverColoredCountries:
                self.drawCountryByCountryParam(country, newRGB)
                self.hoverColoredCountries.remove(country)
        # print("after - player0:", self.player0.hoverColoredCountries)
        # print("after - player1:", self.player1.hoverColoredCountries)

    def drawCountryByCountryParam(self, country, newRGB):
        countryPixelsFile = open(f"countries\\{self.CONTINENT}\\{country}\\pixels.txt", "r")
        countryPixels = countryPixelsFile.readlines()
        for pixel in countryPixels:
            p = pixel.split()
            x = int(p[0])
            y = int(p[1])
            self.window.set_at((x, y), newRGB)

    def initColors(self):
        fileInitPixel = open("countries\\init\\initPixel.txt", "r")
        initPixelLines = fileInitPixel.readlines()
        for initPixelLine in initPixelLines:
            resultInitPixel = initPixelLine.split()
            initPixelCountry = resultInitPixel[0]
            x = int(resultInitPixel[1])
            y = int(resultInitPixel[2])
            fileInitRGB = open("countries\\init\\initRGB.txt", "r")
            initRGBLines = fileInitRGB.readlines()
            for initRGBLine in initRGBLines:
                resultInitRGB = initRGBLine.split()
                initRGBCountry = resultInitRGB[0]
                r = int(resultInitRGB[1])
                g = int(resultInitRGB[2])
                b = int(resultInitRGB[3])
                if initPixelCountry == initRGBCountry:
                    self.drawCountry(initRGBCountry, (r, g, b))

    def changeOptionIfArrowClicked(self, mouseX, mouseY):
        arrowname = ""
        treeFilename = mouseX // 100 * 100
        treeFile = open(f"tree\\others\\pixels\\{treeFilename}.txt", "r")
        rows = treeFile.readlines()
        for row in rows:
            result = row.split()
            xCord = result[0]
            yCord = result[1]
            if int(xCord) == mouseX and int(yCord) == mouseY:
                arrowname = result[2]
                break
        if arrowname == "":
            return
        # change the flag
        if self.isMultiplayer is False:
            if arrowname == "arrow_right_single_player":
                self.getNextOption()
            elif arrowname == "arrow_left_single_player":
                self.getPreviousOption()
        else:
            if self.playerId == "0" and arrowname == "arrow_right_player0":
                self.getNextOption()
            if self.playerId == "0" and arrowname == "arrow_left_player0":
                self.getPreviousOption()
            if self.playerId == "1" and arrowname == "arrow_right_player1":
                self.getNextOption()
            if self.playerId == "1" and arrowname == "arrow_left_player1":
                self.getPreviousOption()

    def getRandomOption(self):
        options = []
        for x in os.walk(f"countries\\{self.CONTINENT}"):
            dataList = x[0].split("\\")
            if len(dataList) < 3:
                continue
            options.append(dataList[2])
        if len(options) == 0:
            return ""
        return random.choice(options)

    def getOptionByIndex(self, index):
        options = []
        for x in os.walk(f"countries\\{self.CONTINENT}"):
            dataList = x[0].split("\\")
            if len(dataList) < 3:
                continue
            options.append(dataList[2])
        if len(options) == 0:
            return ""
        return options[index]

    def getNextOption(self):
        options = []
        for x in os.walk(f"countries\\{self.CONTINENT}"):
            dataList = x[0].split("\\")
            if len(dataList) < 3:
                continue
            options.append(dataList[2])
        if len(options) == 0:
            return
        if self.isMultiplayer:
            if self.playerId == self.player0.id:
                indexCurrentOption = 0
                for correctOption in self.player0.correctOptions:
                    if correctOption in options:
                        options.remove(correctOption)
                if self.player0.currentOption in options:
                    indexCurrentOption = options.index(self.player0.currentOption)
                else:
                    indexCurrentOption = len(options) // 2
                if indexCurrentOption + 1 >= len(options):
                    self.player0.currentOption = options[0]
                else:
                    self.player0.currentOption = options[indexCurrentOption + 1]
                self.displayOptionData()
            else:
                indexCurrentOption = 0
                for correctOption in self.player1.correctOptions:
                    if correctOption in options:
                        options.remove(correctOption)
                if self.player1.currentOption in options:
                    indexCurrentOption = options.index(self.player1.currentOption)
                else:
                    indexCurrentOption = len(options) // 2
                if indexCurrentOption + 1 >= len(options):
                    self.player1.currentOption = options[0]
                else:
                    self.player1.currentOption = options[indexCurrentOption + 1]
                self.displayOptionData()
        else:
            indexCurrentOption = 0
            for correctOption in self.correctOptions:
                if correctOption in options:
                    options.remove(correctOption)
            if self.currentOption in options:
                indexCurrentOption = options.index(self.currentOption)
            else:
                indexCurrentOption = len(options) // 2
            if indexCurrentOption + 1 >= len(options):
                self.currentOption = options[0]
            else:
                self.currentOption = options[indexCurrentOption + 1]
            self.displayOptionData()

    def getPreviousOption(self):
        options = []
        for x in os.walk(f"countries\\{self.CONTINENT}"):
            dataList = x[0].split("\\")
            if len(dataList) < 3:
                continue
            options.append(dataList[2])
        if len(options) == 0:
            return
        if self.isMultiplayer:
            if self.playerId == self.player0.id:
                indexCurrentOption = 0
                for correctOption in self.player0.correctOptions:
                    if correctOption in options:
                        options.remove(correctOption)
                if self.player0.currentOption in options:
                    indexCurrentOption = options.index(self.player0.currentOption)
                else:
                    indexCurrentOption = len(options) // 2
                if indexCurrentOption <= 0:
                    self.player0.currentOption = options[len(options) - 1]
                else:
                    self.player0.currentOption = options[indexCurrentOption - 1]
                self.displayOptionData()
            else:
                indexCurrentOption = 0
                for correctOption in self.player1.correctOptions:
                    if correctOption in options:
                        options.remove(correctOption)
                if self.player1.currentOption in options:
                    indexCurrentOption = options.index(self.player1.currentOption)
                else:
                    indexCurrentOption = len(options) // 2
                if indexCurrentOption <= 0:
                    self.player1.currentOption = options[len(options) - 1]
                else:
                    self.player1.currentOption = options[indexCurrentOption - 1]
                self.displayOptionData()
        else:
            indexCurrentOption = 0
            for correctOption in self.correctOptions:
                if correctOption in options:
                    options.remove(correctOption)
            if self.currentOption in options:
                indexCurrentOption = options.index(self.currentOption)
            else:
                indexCurrentOption = len(options) // 2
            if indexCurrentOption <= 0:
                self.currentOption = options[len(options) - 1]
            else:
                self.currentOption = options[indexCurrentOption - 1]
            self.displayOptionData()

    def displayArrows(self, xCoord, yCoord):
        arrow_right = pygame.image.load("arrow_right.png")
        arrow_right = pygame.transform.scale(arrow_right, (80, 65))
        self.window.blit(arrow_right, (xCoord + 1090, yCoord + 255))

        arrow_left = pygame.image.load("arrow_left.png")
        arrow_left = pygame.transform.scale(arrow_left, (80, 65))
        self.window.blit(arrow_left, (xCoord + 1020, yCoord + 255))

    def displayTimeLeft(self):
        RED = (255, 0, 0)
        font = pygame.font.Font(None, 33)
        text_surface = font.render("Time Left: 13:09", True, RED)
        self.window.blit(text_surface, (1015, 115))

    def displayCurrentGameTitle(self):
        BLACK = (0, 0, 0)
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Countries game", True, BLACK)
        self.window.blit(text_surface, (965, 50))

    def displayOptionData(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        big_font = pygame.font.Font(None, 34)
        font = pygame.font.Font(None, 30)
        if not self.isMultiplayer:
            self.displayOption(+10, 170)
            self.displayArrows(+10, 170)
            text_surface = font.render("Your score: 2/30", True, BLACK)
            self.window.blit(text_surface, (1020, 405))
        else:
            self.drawScoreRect()
            # player0 data
            self.displayOption(+10, 70, self.player0.currentOption)
            self.displayArrows(+10, 70)
            text_surface0 = font.render(f"Daniel: {len(self.player0.correctOptions)}/30", True, BLACK)
            self.window.blit(text_surface0, (1040, 305))

            # player1 data
            self.displayOption(+10, 310, self.player1.currentOption)
            self.displayArrows(+10, 310)
            text_surface1 = font.render(f"Claudiu: {len(self.player1.correctOptions)}/30", True, BLACK)
            self.window.blit(text_surface1, (1040, 545))

    def drawScoreRect(self):
        rect_size = (160, 22)
        rect_color = (255, 255, 255)
        rect1_position = (1040, 302)
        rect2_position = (1040, 542)

        # Draw the rectangle
        pygame.draw.rect(self.window, rect_color, pygame.Rect(rect1_position, rect_size))
        pygame.draw.rect(self.window, rect_color, pygame.Rect(rect2_position, rect_size))

    def drawAnOval(self, text, xCoord, yCoord):
        # circle

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        # draw circle
        # radius = 100
        # center = (1100, 500)
        # pygame.draw.circle(window, RED, center, radius)

        # draw oval

        rect = pygame.Rect(xCoord + 990, yCoord + 100, 200, 120)  # left, top, width, height
        pygame.draw.ellipse(self.window, BLACK, rect, width=20)
        pygame.draw.ellipse(self.window, RED, rect.inflate(-9, -9))

        # add text to oval
        font = pygame.font.Font(None, 34)
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + " " + word)[0] < rect.width - 20:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        y = rect.top + 55 - (len(lines) * 10)
        for line in lines:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(centerx=rect.centerx, y=y)
            self.window.blit(text_surface, text_rect)
            y += font.size(line)[1]

    def getCapital(self, option):
        capital = ""
        if self.isMultiplayer:
            if option != "":
                countryFile = open(f"countries\\{self.CONTINENT}\\{option}\\country.txt", "r")
            elif self.playerId == self.player0.id:
                capitalFile = open(f"countries\\{self.CONTINENT}\\{self.player0.currentOption}\\country.txt", "r")
            else:
                capitalFile = open(f"countries\\{self.CONTINENT}\\{self.player1.currentOption}\\country.txt", "r")
        else:
            capitalFile = open(f"countries\\{self.CONTINENT}\\{self.currentOption}\\country.txt", "r")
        rows = capitalFile.readlines()
        for row in rows:
            result = row.split()
            if len(result) > 2:
                if result[0] == self.language:
                    for index in range(2, len(result)):
                        capital = capital + result[index] + " "
                    break
        return capital

    def getCountry(self, option=""):
        country = ""
        if self.isMultiplayer:
            if option != "":
                countryFile = open(f"countries\\{self.CONTINENT}\\{option}\\country.txt", "r")
            elif self.playerId == self.player0.id:
                countryFile = open(f"countries\\{self.CONTINENT}\\{self.player0.currentOption}\\country.txt", "r")
            else:
                countryFile = open(f"countries\\{self.CONTINENT}\\{self.player1.currentOption}\\country.txt", "r")
        else:
            countryFile = open(f"countries\\{self.CONTINENT}\\{self.currentOption}\\country.txt", "r")
        rows = countryFile.readlines()
        for row in rows:
            result = row.split()
            if len(result) > 2:
                if result[0] == self.language:
                    for index in range(2, len(result)):
                        country = country + result[index] + " "
                    break
        return country

    def displayCapital(self, xCoord, yCoord, option=""):
        capital = self.getCapital(option)
        self.drawAnOval(capital, xCoord, yCoord)

    def displayCountry(self, xCoord, yCoord, option=""):
        country = self.getCountry(option)
        self.drawAnOval(country, xCoord, yCoord)

    def displayFlag(self, xCoord, yCoord, optionParam=""):
        if self.isMultiplayer:
            if optionParam != "":
                option = pygame.image.load(f"countries\\{self.CONTINENT}\\{optionParam}\\flag.png")
            elif self.playerId == self.player0.id:
                option = pygame.image.load(f"countries\\{self.CONTINENT}\\{self.player0.currentOption}\\flag.png")
            else:
                option = pygame.image.load(f"countries\\{self.CONTINENT}\\{self.player1.currentOption}\\flag.png")
        else:
            option = pygame.image.load(f"countries\\{self.CONTINENT}\\{self.currentOption}\\flag.png")
        option = pygame.transform.scale(option, (130, 100))  # 130, 100 for flags
        self.window.blit(option, (xCoord + 1020, yCoord + 200))  # 1020, 200 for flags

    def displayOption(self, xCoord, yCoord, option=""):
        if self.gameType == self.gameTypeFlags:
            self.displayFlag(xCoord, yCoord, option)
        if self.gameType == self.gameTypeCapitals:
            self.displayCapital(xCoord, yCoord, option)
        if self.gameType == self.gameTypeCountries:
            self.displayCountry(xCoord, yCoord, option)

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def play(self):
        self.playGame()
        # while True:
        #     PLAY_MOUSE_POS = pygame.mouse.get_pos()
        #
        #     window.fill("black")
        #
        #     PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        #     PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        #     window.blit(PLAY_TEXT, PLAY_RECT)
        #
        #     PLAY_BACK = Button(image=None, pos=(640, 460),
        #                        text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        #
        #     PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        #     PLAY_BACK.update(window)
        #
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
        #                 main_menu()
        #
        #     pygame.display.update()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.window.fill("white")

            OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            self.window.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 460),
                                  text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        while True:
            self.window.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")

            self.window.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        # play()
                        self.continentsMenu()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def continentsMenu(self):
        while True:
            self.window.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            EUROPE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                   text_input="EUROPE", font=self.get_font(75), base_color="#d7fcd4",
                                   hovering_color="White")
            AFRICA_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550),
                                   text_input="AFRICA", font=self.get_font(75), base_color="#d7fcd4",
                                   hovering_color="White")

            self.window.blit(MENU_TEXT, MENU_RECT)

            for button in [EUROPE_BUTTON, AFRICA_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if EUROPE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.playGame()
                    if AFRICA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.playGame()

            pygame.display.update()

    def load_camera(self):
        self.frame, self.img = self.cap.read()

    def saveState(self):
        cropped_rect = pygame.Rect(20, 20, 897, 680)
        cropped_surface = self.window.subsurface(cropped_rect)
        realSize = (self.mapRealWidth, self.mapRealHeight)
        cropped_surface = pygame.transform.scale(cropped_surface, realSize)
        pygame.image.save(cropped_surface, "state/cropped_image.png")

    def redrawWindow(self):
        yellow = (238, 224, 29)
        green = (23, 165, 23)
        blue1 = (0, 51, 153)
        self.window.fill((255, 255, 255))
        bg_img = pygame.image.load("state/cropped_image.png")
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.window.blit(bg_img, (20, 20), )
        # mouse
        # cursor_img = pygame.image.load("cursor1.png")
        # cursor_img = pygame.transform.scale(cursor_img, (50, 40))

        self.displayOptionData()
        self.displayCurrentGameTitle()
        self.displayTimeLeft()

    def drawMouse(self):
        cursor_img = pygame.image.load("cursor1.png")
        cursor_img = pygame.transform.scale(cursor_img, (50, 40))

    def playGame(self):
        handTrackingModule = HandTrackingModule.HandDetector()
        # hand.show()
        # self.c_thread=threading.Thread(target=hand.show, args=())
        # self.c_thread.start()
        # print("hello, thread")
        yellow = (238, 224, 29)
        green = (23, 165, 23)
        blue1 = (0, 51, 153)
        self.window.fill((255, 255, 255))
        bg_img = pygame.image.load(self.currentMap)
        self.mapRealWidth = bg_img.get_width()
        self.mapRealHeight = bg_img.get_height()
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.window.blit(bg_img, (20, 20), )

        # mouse
        cursor_img = pygame.image.load("cursor1.png")
        cursor_img = pygame.transform.scale(cursor_img, (50, 40))

        self.currentOption = self.getRandomOption()
        # self.displayOption()
        #
        # arrow_right = pygame.image.load("arrow_right.png")
        # arrow_right = pygame.transform.scale(arrow_right, (80, 65))
        # self.window.blit(arrow_right, (1170, 215))
        #
        # arrow_left = pygame.image.load("arrow_left.png")
        # arrow_left = pygame.transform.scale(arrow_left, (80, 65))
        # self.window.blit(arrow_left, (920, 215))

        self.displayOptionData()
        self.displayCurrentGameTitle()
        self.displayTimeLeft()

        self.computerVision = True

        arrowColor = (34, 177, 76)
        runing = True
        self.saveState()
        while runing:
            self.load_camera()
            newScannedHandsImg = handTrackingModule.findHands(self.img)
            handCoords = handTrackingModule.getCoords(newScannedHandsImg)
            if handCoords != None:
                self.cvx = handCoords[0]
                self.cvy = handCoords[1]
                self.redrawWindow()
                self.undrawCountries(blue1)
                self.drawCountry(self.cvx, self.cvy, blue1, yellow)
                self.window.blit(cursor_img, (handCoords[0], handCoords[1]), )
            elif self.cvx > 0 or self.cvy > 0:
                self.window.blit(cursor_img, (self.cvx, self.cvy), )
            if handTrackingModule.isHandClosed():
                self.redrawWindow()
                self.changeOptionIfArrowClicked(self.cvx, self.cvy)
                self.displayOptionData()
                self.drawCorrectCountry(self.cvx, self.cvy, yellow, green)

                # self.initTreePixels()
                # self.writeCountryPixelsInFile("arrow_left_player1", pos[0], pos[1])
            cv2.imshow("Camera", newScannedHandsImg)
            cv2.waitKey(1)
            ev = pygame.event.get()
            # for event in ev:
            #
            #     if event.type == pygame.MOUSEMOTION:  # MOUSEBUTTONUP MOUSEMOTION
            #         pos = pygame.mouse.get_pos()
            #         self.undrawCountries(blue1)
            #         self.drawCountry(pos[0], pos[1], blue1, yellow)
            #     if event.type == pygame.MOUSEBUTTONUP:
            #         pos = pygame.mouse.get_pos()
            #         self.changeOptionIfArrowClicked(pos[0], pos[1])
            #         self.displayOptionData()
            #         self.drawCorrectCountry(pos[0], pos[1], yellow, green)
            #
            #         # self.initTreePixels()
            #         # self.writeCountryPixelsInFile("arrow_left_player1", pos[0], pos[1])
            pygame.display.update()
        pygame.quit()

    def launch(self):
        pygame.init()
        pygame.display.set_caption("Menu")
        self.cap = cv2.VideoCapture(0)
        self.frame = self.cap.read()
        self.playGame()
        # main_menu()
