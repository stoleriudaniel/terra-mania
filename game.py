import cv2.data
import HandTrackingModule
from InputText import InputText
from client import Client
import os
import random
from pathlib import Path
import subprocess
import pygame
import sys
from player import Player
from button import Button
import psutil


class Game:

    def __init__(self):
        self.playerId = 0
        self.player0 = Player(0, 0, "0")
        self.player1 = Player(0, 0, "1")
        self.isMultiplayer = False
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.maps = ['Europe_map1.png', 'south_america112.png', 'north-america111.png', 'asia1.png', 'africa111.png',
                     'oceania111.png']
        self.continents = ["Europe", "South-America", "North-America", "Asia", "Africa", "Oceania"]
        self.CONTINENT = self.continents[3]
        self.currentMap = self.maps[3]

        self.indexMapAndContinent = 0

        self.language = "English"

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

        self.computerVision = True
        self.gameTime = "none"

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

    def getAllOptionsOfTheContinent(self):
        directories = [x[0] for x in os.walk(f"countries\\{self.CONTINENT}")]
        return len(directories) - 1

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
        if self.isMultiplayer:
            if self.player0.id == playerIdParam:
                if country == self.player0.currentOption or country == self.player0.lastCorrectOption:
                    self.player0.lastCorrectOption = country
                    self.drawCountryByCountryParam(country, newRgb)
                    self.player0.hoverColoredCountries.remove(country)
                    self.player0.correctOptions.append(country)
                    self.getNextOption()
                else:
                    self.player0.incorrectCountries.append(country)
                    red = (255, 0, 0)
                    self.drawCountryByCountryParam(country, red)
                    self.player0.hoverColoredCountries.remove(country)
            elif self.player1.id == playerIdParam:
                if country == self.player1.currentOption or country == self.player1.lastCorrectOption:
                    self.player1.lastCorrectOption = country
                    self.drawCountryByCountryParam(country, newRgb)
                    self.player1.hoverColoredCountries.remove(country)
                    self.player1.correctOptions.append(country)
                    self.getNextOption()
                else:
                    self.player1.incorrectCountries.append(country)
                    red = (255, 0, 0)
                    self.drawCountryByCountryParam(country, red)
                    self.player1.hoverColoredCountries.remove(country)
            self.player0.correctOptions = list(dict.fromkeys(self.player0.correctOptions))
            self.player1.correctOptions = list(dict.fromkeys(self.player1.correctOptions))
        else:
            if country == self.currentOption:
                self.drawCountryByCountryParam(country, newRgb)
                if country in self.hoverColoredCountries:
                    self.hoverColoredCountries.remove(country)
                self.correctOptions.append(country)
                self.getNextOption()
                if self.computerVision:
                    self.saveState()
            else:
                self.incorrectCountries.append(country)
                red = (255, 0, 0)
                self.drawCountryByCountryParam(country, red)
                if country in self.hoverColoredCountries:
                    self.hoverColoredCountries.remove(country)

    def undrawCountries(self, newRGB):
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
        arrow_right = pygame.image.load("assets/arrows/arrow_right.png")
        arrow_right = pygame.transform.scale(arrow_right, (80, 65))
        self.window.blit(arrow_right, (xCoord + 1090, yCoord + 255))

        arrow_left = pygame.image.load("assets/arrows/arrow_left.png")
        arrow_left = pygame.transform.scale(arrow_left, (80, 65))
        self.window.blit(arrow_left, (xCoord + 1020, yCoord + 255))

    def displayTimeLeft(self):
        rect_size = (260, 50)
        rect_color = (255, 255, 255)
        rect1_position = (970, 100)

        # Draw the rectangle
        pygame.draw.rect(self.window, rect_color, pygame.Rect(rect1_position, rect_size))

        RED = (255, 0, 0)
        font = pygame.font.Font(None, 33)
        text_surface = font.render(f"Time Left: {self.gameTime}", True, RED)
        self.window.blit(text_surface, (1015, 115))

    def displayCurrentGameTitle(self):
        BLACK = (0, 0, 0)
        font = pygame.font.Font(None, 50)
        text_surface = font.render(f"{self.gameType.capitalize()} game", True, BLACK)
        self.window.blit(text_surface, (965, 50))

    def displayOptionData(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        big_font = pygame.font.Font(None, 34)
        font = pygame.font.Font(None, 30)
        rect_size = (340, 37)
        rect_color = WHITE
        rect1_position = (930, 395)
        rect2_position = (930, 295)
        rect3_position = (930, 535)
        if not self.isMultiplayer:
            self.displayOption(+10, 170)
            self.displayArrows(+10, 170)

            # Draw the rectangle
            pygame.draw.rect(self.window, rect_color, pygame.Rect(rect1_position, rect_size))
            text_surface = font.render(f"Your score: {len(self.correctOptions)}/{self.getAllOptionsOfTheContinent()}", True, BLACK)
            self.window.blit(text_surface, (1020, 405))
        else:
            self.drawScoreRect()
            # player0 data
            self.displayOption(+10, 70, self.player0.currentOption)
            self.displayArrows(+10, 70)
            pygame.draw.rect(self.window, rect_color, pygame.Rect(rect2_position, rect_size))
            text_surface0 = font.render(f"{self.player0.nickname}: {len(self.player0.correctOptions)}/{self.getAllOptionsOfTheContinent()}", True, BLACK)
            self.window.blit(text_surface0, (1040, 305))

            # player1 data
            self.displayOption(+10, 310, self.player1.currentOption)
            self.displayArrows(+10, 310)
            pygame.draw.rect(self.window, rect_color, pygame.Rect(rect3_position, rect_size))
            text_surface1 = font.render(f"{self.player1.nickname}: {len(self.player1.correctOptions)}/{self.getAllOptionsOfTheContinent()}", True, BLACK)
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
                capitalFile = open(f"countries\\{self.CONTINENT}\\{option}\\country.txt", "r")
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
        self.window.blit(option, (xCoord + 1025, yCoord + 120))  # 1020, 200 for flags

    def displayOption(self, xCoord, yCoord, option=""):
        if self.gameType == self.gameTypeFlags:
            self.displayFlag(xCoord, yCoord, option)
        if self.gameType == self.gameTypeCapitals:
            self.displayCapital(xCoord, yCoord, option)
        if self.gameType == self.gameTypeCountries:
            self.displayCountry(xCoord, yCoord, option)

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/fonts/font.ttf", size)

    def options(self):
        return

    def load_camera(self):
        self.frame, self.img = self.cap.read()

    def saveState(self):
        cropped_rect = pygame.Rect(20, 20, 897, 680)
        cropped_surface = self.window.subsurface(cropped_rect)
        # realSize = (self.mapRealWidth, self.mapRealHeight)
        # cropped_surface = pygame.transform.scale(cropped_surface, realSize)
        pygame.image.save(cropped_surface, "state/cropped_image.png")

    def redrawWindow(self):
        self.window.fill((255, 255, 255))
        bg_img = pygame.image.load("state/cropped_image.png")
        self.window.blit(bg_img, (20, 20), )

        self.displayOptionData()
        self.displayCurrentGameTitle()

    def singlePlayerPause(self):
        backgroundImage = pygame.image.load("assets/menu/6.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(40).render("Game is paused", True, "#d7fcd4")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 270))

            RESUME_BUTTON = Button(image=None, pos=(640, 465),
                                 text_input="Resume", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [RESUME_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                        return

            pygame.display.update()

    def singlePlayerQuit(self):
        backgroundImage = pygame.image.load("assets/menu/5.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(30).render("Do you want to quit?", True, "#d7fcd4")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 230))

            NO_BUTTON = Button(image=None, pos=(640, 390),
                                 text_input="No", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            YES_BUTTON = Button(image=None, pos=(640, 505),
                                 text_input="Yes", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [YES_BUTTON, NO_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NO_BUTTON.checkForInput(MENU_MOUSE_POS):
                        return
                    if YES_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if self.computerVision:
                            self.cap.release()
                            cv2.destroyAllWindows()
                        self.originalMainMenu()

            pygame.display.update()

    def playGame(self):
        try:
            handTrackingModule = HandTrackingModule.HandDetector()
            yellow = (238, 224, 29)
            green = (23, 165, 23)
            blue1 = (0, 51, 153)
            self.window.fill((255, 255, 255))
            bg_img = pygame.image.load(f"assets/continents/{self.currentMap}")
            self.mapRealWidth = bg_img.get_width()
            self.mapRealHeight = bg_img.get_height()
            bg_img = pygame.transform.scale(bg_img, (897, 680))
            self.window.blit(bg_img, (20, 20), )

            # mouse
            cursor_img = pygame.image.load("assets/cursor/cursor.png")
            cursor_img = pygame.transform.scale(cursor_img, (50, 40))

            self.currentOption = self.getRandomOption()

            self.displayOptionData()
            self.displayCurrentGameTitle()

            PAUSE_BUTTON = Button(image=None, pos=(1030, 655),
                                 text_input="Pause", font=self.get_font(30), base_color="Red",
                                 hovering_color="Blue")
            QUIT_BUTTON = Button(image=None, pos=(1190, 655),
                                 text_input="Quit", font=self.get_font(30), base_color="Red",
                                 hovering_color="Blue")

            # self.singlePlayerQuitButton()
            self.correctOptions = []

            runing = True

            # self.computerVision = True

            if self.computerVision:
                self.cap = cv2.VideoCapture(0)
                self.frame = self.cap.read()
                self.saveState()
            while runing:

                MENU_MOUSE_POS = pygame.mouse.get_pos()
                for button in [QUIT_BUTTON, PAUSE_BUTTON]:
                    button.changeColor(MENU_MOUSE_POS)
                    button.update(self.window)


                if self.computerVision:
                    self.load_camera()
                    newScannedHandsImg = handTrackingModule.findHands(self.img)
                    handCoords = handTrackingModule.getCoords(newScannedHandsImg)
                    if handCoords != None:
                        self.cvx = self.SCREEN_WIDTH - handCoords[0]
                        self.cvy = handCoords[1]
                        if self.cvx > 0 and self.cvx < self.SCREEN_WIDTH and self.cvy > 0 and self.cvy < self.SCREEN_HEIGHT:
                            self.redrawWindow()
                            MENU_MOUSE_POS = pygame.mouse.get_pos()
                            for button in [QUIT_BUTTON, PAUSE_BUTTON]:
                                button.changeColor(MENU_MOUSE_POS)
                                button.update(self.window)
                            self.undrawCountries(blue1)
                            self.drawCountry(self.cvx, self.cvy, blue1, yellow)
                            self.window.blit(cursor_img, (self.cvx, self.cvy), )
                    elif self.cvx > 0 or self.cvy > 0:
                        if self.cvx > 0 and self.cvx < self.SCREEN_WIDTH and self.cvy > 0 and self.cvy < self.SCREEN_HEIGHT:
                            self.window.blit(cursor_img, (self.cvx, self.cvy), )
                    if handTrackingModule.isHandClosed():
                        if self.cvx > 0 and self.cvx < self.SCREEN_WIDTH and self.cvy > 0 and self.cvy < self.SCREEN_HEIGHT:
                            if QUIT_BUTTON.checkForInput((self.cvx, self.cvy)):
                                self.saveState()
                                self.singlePlayerQuit()
                                self.redrawWindow()
                                self.cvx, self.cvy = 0, 0
                            if PAUSE_BUTTON.checkForInput((self.cvx, self.cvy)):
                                self.saveState()
                                self.singlePlayerPause()
                                self.redrawWindow()
                                self.cvx, self.cvy = 0, 0
                                MENU_MOUSE_POS = pygame.mouse.get_pos()
                                for button in [QUIT_BUTTON, PAUSE_BUTTON]:
                                    button.changeColor(MENU_MOUSE_POS)
                                    button.update(self.window)
                            self.redrawWindow()
                            MENU_MOUSE_POS = pygame.mouse.get_pos()
                            for button in [QUIT_BUTTON, PAUSE_BUTTON]:
                                button.changeColor(MENU_MOUSE_POS)
                                button.update(self.window)
                            self.changeOptionIfArrowClicked(self.cvx, self.cvy)
                            self.displayOptionData()
                            self.drawCorrectCountry(self.cvx, self.cvy, blue1, green)
                            self.window.blit(cursor_img, (self.cvx, self.cvy), )
                        # self.initTreePixels()
                        # self.writeCountryPixelsInFile("arrow_left_player1", pos[0], pos[1])
                    newScannedHandsImg = cv2.flip(newScannedHandsImg, 1)
                    cv2.imshow("Camera", newScannedHandsImg)
                    cv2.waitKey(1)
                else:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.MOUSEMOTION:  # MOUSEBUTTONUP MOUSEMOTION
                            pos = pygame.mouse.get_pos()
                            self.undrawCountries(blue1)
                            self.drawCountry(pos[0], pos[1], blue1, yellow)
                        if event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            self.changeOptionIfArrowClicked(pos[0], pos[1])
                            self.displayOptionData()
                            self.drawCorrectCountry(pos[0], pos[1], yellow, green)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                                self.saveState()
                                self.singlePlayerQuit()
                                self.redrawWindow()
                                self.cvx, self.cvy = 0, 0
                            if PAUSE_BUTTON.checkForInput(MENU_MOUSE_POS):
                                self.saveState()
                                self.singlePlayerPause()
                                self.redrawWindow()
                            # self.initTreePixels()
                            # self.writeCountryPixelsInFile("arrow_left_player1", pos[0], pos[1])
                pygame.display.update()
            pygame.quit()
        except:
            if self.computerVision:
                self.cap.release()
                cv2.destroyAllWindows()
            if len(self.correctOptions) == self.getAllOptionsOfTheContinent():
                self.window.fill((255, 255, 255))
                bg_img = pygame.image.load(f"assets/menu/8.jpg")
                bg_img = pygame.transform.scale(bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                win = "You win!"
                while True:
                    self.window.blit(bg_img, (0, 0), )
                    MENU_MOUSE_POS = pygame.mouse.get_pos()
                    MENU_TEXT = self.get_font(40).render("Game is ended.", True, "#d7fcd4")
                    MENU_RECT = MENU_TEXT.get_rect(center=(640, 220))
                    self.window.blit(MENU_TEXT, MENU_RECT)

                    WIN_TEXT = self.get_font(30).render(win, True, "Green")
                    WIN_RECT = WIN_TEXT.get_rect(center=(640, 360))
                    self.window.blit(WIN_TEXT, WIN_RECT)

                    BACK_BUTTON = Button(image=None, pos=(640, 532),
                                         text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                         hovering_color="Blue")
                    # self.window.blit(MENU_TEXT, MENU_RECT)
                    for button in [BACK_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(self.window)

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                                self.originalMainMenu()

                    pygame.display.update()
            else:
                self.originalMainMenu()


    def originalMainMenu(self):
        backgroundImage = pygame.image.load("assets/menu/1.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.isMultiplayer = False
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=None, pos=(280, 655),
                                 text_input="Play", font=self.get_font(30), base_color="#d7fcd4",
                                 hovering_color="Blue")
            OPTIONS_BUTTON = Button(image=None, pos=(640, 655),
                                    text_input="Options", font=self.get_font(30), base_color="#d7fcd4",
                                    hovering_color="Blue")
            QUIT_BUTTON = Button(image=None, pos=(1005, 655),
                                 text_input="Quit", font=self.get_font(30), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
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
                        # self.continentsMenu()
                        self.singlePlayerOrMultiplayerMenu()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def singlePlayerOrMultiplayerMenu(self):
        backgroundImage = pygame.image.load("assets/menu/2.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            SINGLEPLAYER_BUTTON = Button(image=None, pos=(640, 215),
                                         text_input="Single Player", font=self.get_font(25), base_color="#d7fcd4",
                                         hovering_color="Blue")
            MULTIPLAYER_BUTTON = Button(image=None, pos=(640, 370),
                                        text_input="Multiplayer", font=self.get_font(25), base_color="#d7fcd4",
                                        hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 528),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.flagsCapitalsCountriesMenu()
                    if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.multiplayerMenu()
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.originalMainMenu()

            pygame.display.update()

    def multiplayerMenu(self):
        backgroundImage = pygame.image.load("assets/menu/2.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CREATE_NEW_SERVER_BUTTON = Button(image=None, pos=(640, 210),
                                              text_input="Create new server", font=self.get_font(25),
                                              base_color="#d7fcd4",
                                              hovering_color="Blue")
            CONNECT_TO_SERVER_BUTTON = Button(image=None, pos=(640, 370),
                                              text_input="Connect to server", font=self.get_font(25),
                                              base_color="#d7fcd4",
                                              hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 528),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [CREATE_NEW_SERVER_BUTTON, CONNECT_TO_SERVER_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CREATE_NEW_SERVER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.flagsCapitalsCountriesServerMenu()
                    if CONNECT_TO_SERVER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.connectToServerMenu()
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.singlePlayerOrMultiplayerMenu()

            pygame.display.update()

    def singlePlayerHandTrackinMenu(self):
        backgroundImage = pygame.image.load("assets/menu/5.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(30).render("Use hand tracking?", True, "#d7fcd4")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 230))

            NO_BUTTON = Button(image=None, pos=(640, 505),
                               text_input="No", font=self.get_font(25), base_color="#d7fcd4",
                               hovering_color="Blue")
            YES_BUTTON = Button(image=None, pos=(640, 390),
                                text_input="Yes", font=self.get_font(25), base_color="#d7fcd4",
                                hovering_color="Blue")
            self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [YES_BUTTON, NO_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NO_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.computerVision = False
                        self.playGame()
                    if YES_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.computerVision = True
                        self.playGame()

            pygame.display.update()

    def createNewServerMenu(self, gameTypeParam, indexMapAndContinent):
        backgroundImage = pygame.image.load("assets/menu/5.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        ipTextFieldSelected = False
        nicknameTextFieldSelected = False
        ip_text = ""
        ip_text_x = 600
        ip_text_y = 200
        ip_text_width = 320
        ip_text_heigth = 50

        nickname_text = ""
        nickname_text_x = 600
        nickname_text_y = 270
        nickname_text_width = 320
        nickname_text_heigth = 50
        color = (255, 255, 255)
        font = pygame.font.Font(None, 40)
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            START_BUTTON = Button(image=None, pos=(640, 390),
                                  text_input="Start", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 502),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")

            text_input = InputText(100, 100, 200, 50)

            for button in [START_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(MENU_MOUSE_POS)
                    if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if len(ip_text) > 0:
                            if ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                        if len(nickname_text) > 0:
                            if nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                        # Server().create()
                        return_code = subprocess.run(
                            ["startServer.bat", ip_text, gameTypeParam, str(indexMapAndContinent)],
                            shell=True).returncode

                        if return_code == 0:
                            print("Server started successfully.")
                            self.gameType = gameTypeParam
                            self.indexMapAndContinent = indexMapAndContinent
                            self.CONTINENT = self.continents[indexMapAndContinent]
                            self.currentMap = self.maps[indexMapAndContinent]
                            client = Client(self, ip_text, nickname_text)
                            client.play()
                            self.originalMainMenu()
                        elif return_code == 1:
                            print("Server is already running. Stopped it and started again.")
                            self.gameType = gameTypeParam
                            self.indexMapAndContinent = indexMapAndContinent
                            self.CONTINENT = self.continents[indexMapAndContinent]
                            self.currentMap = self.maps[indexMapAndContinent]
                            client = Client(self, ip_text, nickname_text)
                            client.play()
                            self.originalMainMenu()
                        else:
                            print("An error occurred while starting the server.")
                        print("create server")
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.multiplayerMenu()
                    if MENU_MOUSE_POS[0] >= ip_text_x and MENU_MOUSE_POS[0] <= ip_text_x + ip_text_width and \
                            MENU_MOUSE_POS[1] >= ip_text_y and MENU_MOUSE_POS[1] <= ip_text_y + ip_text_heigth:
                        ipTextFieldSelected = True
                        if len(ip_text) == 0:
                            ip_text = ip_text + "|"
                        elif ip_text[-1] != "|":
                            ip_text = ip_text + "|"
                    else:
                        if ipTextFieldSelected is True:
                            if len(ip_text) > 0 and ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                            ipTextFieldSelected = False
                    if MENU_MOUSE_POS[0] >= nickname_text_x and MENU_MOUSE_POS[0] <= nickname_text_x + nickname_text_width and \
                            MENU_MOUSE_POS[1] >= nickname_text_y and MENU_MOUSE_POS[1] <= nickname_text_y + nickname_text_heigth:
                        nicknameTextFieldSelected = True
                        if len(nickname_text) == 0:
                            nickname_text = nickname_text + "|"
                        elif nickname_text[-1] != "|":
                            nickname_text = nickname_text + "|"
                    else:
                        if nicknameTextFieldSelected is True:
                            if len(nickname_text) > 0 and nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                            nicknameTextFieldSelected = False
                if event.type == pygame.KEYDOWN:
                    print("key down")
                    if ipTextFieldSelected is True:
                        print("Yes, modify")
                        if event.key == pygame.K_RETURN:
                            # Clear the input text when the user presses enter
                            if len(ip_text) > 0 and ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                            return_code = subprocess.run(
                                ["startServer.bat", ip_text, gameTypeParam, str(indexMapAndContinent)],
                                shell=True).returncode

                            if return_code == 0:
                                print("Server started successfully.")
                                self.gameType = gameTypeParam
                                self.indexMapAndContinent = indexMapAndContinent
                                self.CONTINENT = self.continents[indexMapAndContinent]
                                self.currentMap = self.maps[indexMapAndContinent]
                                client = Client(self, ip_text, nickname_text)
                                client.play()
                                self.originalMainMenu()
                            elif return_code == 1:
                                print("Server is already running. Stopped it and started again.")
                                self.gameType = gameTypeParam
                                self.indexMapAndContinent = indexMapAndContinent
                                self.CONTINENT = self.continents[indexMapAndContinent]
                                self.currentMap = self.maps[indexMapAndContinent]
                                client = Client(self, ip_text, nickname_text)
                                client.play()
                                self.originalMainMenu()
                            else:
                                print("An error occurred while starting the server.")
                            print("create server")
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove the last character when the user presses backspace
                            if ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                                ip_text = ip_text[:-1]
                                ip_text = ip_text + "|"
                        else:
                            # Add the pressed character to the text
                            if ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                                ip_text += event.unicode
                                ip_text = ip_text + "|"
                    if nicknameTextFieldSelected is True:
                        print("Yes, modify")
                        if event.key == pygame.K_RETURN:
                            # Clear the input text when the user presses enter
                            if len(nickname_text) > 0 and nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                            return_code = subprocess.run(
                                ["startServer.bat", nickname_text, gameTypeParam, str(indexMapAndContinent)],
                                shell=True).returncode

                            if return_code == 0:
                                print("Server started successfully.")
                                self.gameType = gameTypeParam
                                self.indexMapAndContinent = indexMapAndContinent
                                self.CONTINENT = self.continents[indexMapAndContinent]
                                self.currentMap = self.maps[indexMapAndContinent]
                                client = Client(self, ip_text, nickname_text)
                                client.play()
                                self.originalMainMenu()
                            elif return_code == 1:
                                print("Server is already running. Stopped it and started again.")
                                self.gameType = gameTypeParam
                                self.indexMapAndContinent = indexMapAndContinent
                                self.CONTINENT = self.continents[indexMapAndContinent]
                                self.currentMap = self.maps[indexMapAndContinent]
                                client = Client(self, ip_text, nickname_text)
                                client.play()
                                self.originalMainMenu()
                            else:
                                print("An error occurred while starting the server.")
                            print("create server")
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove the last character when the user presses backspace
                            if nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                                nickname_text = nickname_text[:-1]
                                nickname_text = nickname_text + "|"
                        else:
                            # Add the pressed character to the text
                            if nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                                nickname_text += event.unicode
                                nickname_text = nickname_text + "|"

            insert_address_text_surface = font.render("Server IP Address:", True, color)
            self.window.blit(insert_address_text_surface, (330 + 5, 205 + 5))

            insert_nickname_text_surface = font.render("Your nickname:", True, color)
            self.window.blit(insert_nickname_text_surface, (330 + 5, 275 + 5))

            # update text input
            text_surface_address = font.render(ip_text, True, color)
            text_surface_nickname = font.render(nickname_text, True, color)

            # Draw the text input object on the screen
            # self.window.fill((20, 20, 0))
            rect_address = pygame.Rect(ip_text_x, ip_text_y, ip_text_width, ip_text_heigth)
            pygame.draw.rect(self.window, color, rect_address, 2)
            self.window.blit(text_surface_address, (ip_text_x + 15, ip_text_y + 12))

            rect_nickname = pygame.Rect(nickname_text_x, nickname_text_y, nickname_text_width, nickname_text_heigth)
            pygame.draw.rect(self.window, color, rect_nickname, 2)
            self.window.blit(text_surface_nickname, (nickname_text_x + 15, nickname_text_y + 12))

            pygame.display.update()

    def connectToServerMenu(self):
        backgroundImage = pygame.image.load("assets/menu/5.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        ipTextFieldSelected = False
        nicknameTextFieldSelected = False
        ip_text = ""
        ip_text_x = 600
        ip_text_y = 200
        ip_text_width = 320
        ip_text_heigth = 50

        nickname_text = ""
        nickname_text_x = 600
        nickname_text_y = 270
        nickname_text_width = 320
        nickname_text_heigth = 50
        color = (255, 255, 255)
        font = pygame.font.Font(None, 40)
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            CONNECT_BUTTON = Button(image=None, pos=(640, 390),
                                    text_input="Connect", font=self.get_font(25), base_color="#d7fcd4",
                                    hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 502),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")

            text_input = InputText(100, 100, 200, 50)

            for button in [CONNECT_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(MENU_MOUSE_POS)
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.multiplayerMenu()
                    if CONNECT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        # Server().create()
                        if len(ip_text) > 0:
                            if ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                        if len(nickname_text) > 0:
                            if nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                        client = Client(self, ip_text, nickname_text)
                        client.play()
                        self.originalMainMenu()
                    if MENU_MOUSE_POS[0] >= ip_text_x and MENU_MOUSE_POS[0] <= ip_text_x + ip_text_width and \
                            MENU_MOUSE_POS[1] >= ip_text_y and MENU_MOUSE_POS[1] <= ip_text_y + ip_text_heigth:
                        ipTextFieldSelected = True
                        if ipTextFieldSelected == False:
                            ipTextFieldSelected = True
                            ip_text = ip_text + "|"
                        if len(ip_text) == 0:
                            ip_text = ip_text + "|"
                        elif ip_text[-1] != "|":
                            ip_text = ip_text + "|"
                    else:
                        if ipTextFieldSelected is True:
                            if len(ip_text) > 0 and ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                            ipTextFieldSelected = False
                    if MENU_MOUSE_POS[0] >= nickname_text_x and MENU_MOUSE_POS[0] <= nickname_text_x + nickname_text_width and \
                            MENU_MOUSE_POS[1] >= nickname_text_y and MENU_MOUSE_POS[1] <= nickname_text_y + nickname_text_heigth:
                        nicknameTextFieldSelected = True
                        if nicknameTextFieldSelected == False:
                            nicknameTextFieldSelected = True
                            nickname_text = nickname_text + "|"
                        if len(nickname_text) == 0:
                            nickname_text = nickname_text + "|"
                        elif nickname_text[-1] != "|":
                            nickname_text = nickname_text + "|"
                    else:
                        if nicknameTextFieldSelected is True:
                            if len(nickname_text) > 0 and nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                            nicknameTextFieldSelected = False
                if event.type == pygame.KEYDOWN:
                    print("key down")
                    if ipTextFieldSelected is True:
                        print("Yes, modify")
                        if event.key == pygame.K_RETURN:
                            # Clear the input text when the user presses enter
                            if len(ip_text) > 0 and ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                            client = Client(self, ip_text, nickname_text)
                            client.play()
                            self.originalMainMenu()
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove the last character when the user presses backspace
                            if ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                                ip_text = ip_text[:-1]
                                ip_text = ip_text + "|"
                        else:
                            # Add the pressed character to the text
                            if ip_text[-1] == "|":
                                ip_text = ip_text[:-1]
                                ip_text += event.unicode
                                ip_text = ip_text + "|"
                    elif nicknameTextFieldSelected is True:
                        print("Yes, modify")
                        if event.key == pygame.K_RETURN:
                            # Clear the input text when the user presses enter
                            if len(nickname_text) > 0 and nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                            client = Client(self, ip_text, nickname_text)
                            client.play()
                            self.originalMainMenu()
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove the last character when the user presses backspace
                            if nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                                nickname_text = nickname_text[:-1]
                                nickname_text = nickname_text + "|"
                        else:
                            # Add the pressed character to the text
                            if nickname_text[-1] == "|":
                                nickname_text = nickname_text[:-1]
                                nickname_text += event.unicode
                                nickname_text = nickname_text + "|"

            insert_address_text_surface = font.render("Server IP Address:", True, color)
            self.window.blit(insert_address_text_surface, (330 + 5, 205 + 5))

            insert_nickname_text_surface = font.render("Your nickname:", True, color)
            self.window.blit(insert_nickname_text_surface, (330 + 5, 275 + 5))

            # update text input
            text_surface_address = font.render(ip_text, True, color)
            text_surface_nickname = font.render(nickname_text, True, color)

            # Draw the text input object on the screen
            # self.window.fill((20, 20, 0))
            rect_address = pygame.Rect(ip_text_x, ip_text_y, ip_text_width, ip_text_heigth)
            pygame.draw.rect(self.window, color, rect_address, 2)
            self.window.blit(text_surface_address, (ip_text_x + 15, ip_text_y + 12))

            rect_nickname = pygame.Rect(nickname_text_x, nickname_text_y, nickname_text_width, nickname_text_heigth)
            pygame.draw.rect(self.window, color, rect_nickname, 2)
            self.window.blit(text_surface_nickname, (nickname_text_x + 15, nickname_text_y + 12))

            pygame.display.update()

    def flagsCapitalsCountriesMenu(self):
        backgroundImage = pygame.image.load("assets/menu/3.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            FLAGS_BUTTON = Button(image=None, pos=(640, 190),
                                  text_input="Flags", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            CAPITALS_BUTTON = Button(image=None, pos=(640, 305),
                                     text_input="Capitals", font=self.get_font(25), base_color="#d7fcd4",
                                     hovering_color="Blue")
            COUNTRIES_BUTTON = Button(image=None, pos=(640, 420),
                                      text_input="Countries", font=self.get_font(25), base_color="#d7fcd4",
                                      hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 535),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [FLAGS_BUTTON, CAPITALS_BUTTON, COUNTRIES_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if FLAGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.continentsMenu(self.gameTypeFlags)
                    if CAPITALS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.continentsMenu(self.gameTypeCapitals)
                    if COUNTRIES_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.continentsMenu(self.gameTypeCountries)
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.singlePlayerOrMultiplayerMenu()

            pygame.display.update()

    def flagsCapitalsCountriesServerMenu(self):
        backgroundImage = pygame.image.load("assets/menu/3.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            FLAGS_BUTTON = Button(image=None, pos=(640, 190),
                                  text_input="Flags", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            CAPITALS_BUTTON = Button(image=None, pos=(640, 305),
                                     text_input="Capitals", font=self.get_font(25), base_color="#d7fcd4",
                                     hovering_color="Blue")
            COUNTRIES_BUTTON = Button(image=None, pos=(640, 420),
                                      text_input="Countries", font=self.get_font(25), base_color="#d7fcd4",
                                      hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 535),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [FLAGS_BUTTON, CAPITALS_BUTTON, COUNTRIES_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if FLAGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.continentsServerMenu(self.gameTypeFlags)
                    if CAPITALS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.continentsServerMenu(self.gameTypeCapitals)
                    if COUNTRIES_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.continentsServerMenu(self.gameTypeCountries)
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.singlePlayerOrMultiplayerMenu()

            pygame.display.update()

    def continentsServerMenu(self, gameTypeParam):
        backgroundImage = pygame.image.load("assets/menu/4.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            NORTH_BUTTON = Button(image=None, pos=(480, 220),
                                  text_input="North", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            AMERICA_N_BUTTON = Button(image=None, pos=(480, 250),
                                      text_input="America", font=self.get_font(25), base_color="#d7fcd4",
                                      hovering_color="Blue")
            SOUTH_BUTTON = Button(image=None, pos=(480, 330),
                                  text_input="South", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            AMERICA_S_BUTTON = Button(image=None, pos=(480, 360),
                                      text_input="America", font=self.get_font(25), base_color="#d7fcd4",
                                      hovering_color="Blue")
            AFRICA_BUTTON = Button(image=None, pos=(480, 455),
                                   text_input="Africa", font=self.get_font(25), base_color="#d7fcd4",
                                   hovering_color="Blue")
            EUROPE_BUTTON = Button(image=None, pos=(800, 235),
                                   text_input="Europe", font=self.get_font(25), base_color="#d7fcd4",
                                   hovering_color="Blue")
            ASIA_BUTTON = Button(image=None, pos=(800, 345),
                                 text_input="Asia", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            OCEANIA_BUTTON = Button(image=None, pos=(800, 455),
                                    text_input="Oceania", font=self.get_font(25), base_color="#d7fcd4",
                                    hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 560),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [AFRICA_BUTTON, ASIA_BUTTON, NORTH_BUTTON, AMERICA_N_BUTTON, SOUTH_BUTTON, AMERICA_S_BUTTON,
                           OCEANIA_BUTTON, EUROPE_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NORTH_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 2)
                    if AMERICA_N_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 2)
                    if SOUTH_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 1)
                    if AMERICA_S_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 1)
                    if AFRICA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 4)
                    if EUROPE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 0)
                    if ASIA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 3)
                    if OCEANIA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.createNewServerMenu(gameTypeParam, 5)
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.singlePlayerOrMultiplayerMenu()

            pygame.display.update()

    def continentsMenu(self, gameTypeParam):
        self.gameType = gameTypeParam
        backgroundImage = pygame.image.load("assets/menu/4.jpg")
        backgroundImageScaled = pygame.transform.scale(backgroundImage, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        while True:
            self.window.blit(backgroundImageScaled, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            NORTH_BUTTON = Button(image=None, pos=(480, 220),
                                  text_input="North", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            AMERICA_N_BUTTON = Button(image=None, pos=(480, 250),
                                      text_input="America", font=self.get_font(25), base_color="#d7fcd4",
                                      hovering_color="Blue")
            SOUTH_BUTTON = Button(image=None, pos=(480, 330),
                                  text_input="South", font=self.get_font(25), base_color="#d7fcd4",
                                  hovering_color="Blue")
            AMERICA_S_BUTTON = Button(image=None, pos=(480, 360),
                                      text_input="America", font=self.get_font(25), base_color="#d7fcd4",
                                      hovering_color="Blue")
            AFRICA_BUTTON = Button(image=None, pos=(480, 455),
                                   text_input="Africa", font=self.get_font(25), base_color="#d7fcd4",
                                   hovering_color="Blue")
            EUROPE_BUTTON = Button(image=None, pos=(800, 235),
                                   text_input="Europe", font=self.get_font(25), base_color="#d7fcd4",
                                   hovering_color="Blue")
            ASIA_BUTTON = Button(image=None, pos=(800, 345),
                                 text_input="Asia", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            OCEANIA_BUTTON = Button(image=None, pos=(800, 455),
                                    text_input="Oceania", font=self.get_font(25), base_color="#d7fcd4",
                                    hovering_color="Blue")
            BACK_BUTTON = Button(image=None, pos=(640, 560),
                                 text_input="Back", font=self.get_font(25), base_color="#d7fcd4",
                                 hovering_color="Blue")
            # self.window.blit(MENU_TEXT, MENU_RECT)
            for button in [AFRICA_BUTTON, ASIA_BUTTON, NORTH_BUTTON, AMERICA_N_BUTTON, SOUTH_BUTTON, AMERICA_S_BUTTON,
                           OCEANIA_BUTTON, EUROPE_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.maps = ['Europe_map1.png', 'south_america112.png', 'north-america111.png', 'asia1.png',
                                 'africa111.png',
                                 'oceania111.png']
                    self.continents = ["Europe", "South-America", "North-America", "Asia", "Africa", "Oceania"]
                    self.CONTINENT = self.continents[3]
                    self.currentMap = self.maps[3]

                    if NORTH_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[2]
                        self.CONTINENT = self.continents[2]
                        self.singlePlayerHandTrackinMenu()
                    if AMERICA_N_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[2]
                        self.CONTINENT = self.continents[2]
                        self.singlePlayerHandTrackinMenu()
                    if SOUTH_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[1]
                        self.CONTINENT = self.continents[1]
                        self.singlePlayerHandTrackinMenu()
                    if AMERICA_S_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[1]
                        self.CONTINENT = self.continents[1]
                        self.singlePlayerHandTrackinMenu()
                    if AFRICA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[4]
                        self.CONTINENT = self.continents[4]
                        self.singlePlayerHandTrackinMenu()
                    if EUROPE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[0]
                        self.CONTINENT = self.continents[0]
                        self.singlePlayerHandTrackinMenu()
                    if ASIA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[3]
                        self.CONTINENT = self.continents[3]
                        self.singlePlayerHandTrackinMenu()
                    if OCEANIA_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.currentMap = self.maps[5]
                        self.CONTINENT = self.continents[5]
                        self.singlePlayerHandTrackinMenu()
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.singlePlayerOrMultiplayerMenu()

            pygame.display.update()

    def launch(self):
        pygame.init()
        pygame.display.set_caption("Terra mania")
        self.originalMainMenu()
