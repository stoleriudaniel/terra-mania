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
        self.player0 = Player(0, 0, 0)
        self.player1 = Player(0, 0, 1)
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
        file = open(f"countries\\{countryName}\\pixels.txt", "w")
        # file = open(f"arrows\\{countryName}\\pixels.txt", "w")
        margin = (0, 0, 0)  # black
        uncolored = (0, 51, 153)  # blue
        newColor = (238, 224, 29)  # yellow
        arrowColor = (34, 177, 76)
        # uncolored = arrowColor
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

    def drawCountry(self, mouseX, mouseY, initRgb, newRgb):
        red = (255, 0, 0)
        country = ""
        c = self.window.get_at((mouseX, mouseY))
        # print((c[0], c[1], c[2]) != initRgb, c)
        if (c[0], c[1], c[2]) != initRgb:
            if (c[0], c[1], c[2]) != red:
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
            self.player0.currentHoveredCountry = country
            self.drawCountryByCountryParam(country, newRgb)
            self.hoverColoredCountries.append(country)
        else:
            self.currentHoveredCountry = country
            self.drawCountryByCountryParam(country, newRgb)
            self.hoverColoredCountries.append(country)

    def drawCorrectCountry(self, mouseX, mouseY, initRgb, newRgb):
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
            if country == self.player0.currentOption:
                self.drawCountryByCountryParam(country, newRgb)
                self.hoverColoredCountries.remove(country)
                self.correctOptions.append(country)
                self.getNextOption()
            else:
                self.incorrectCountries.append(country)
                red = (255, 0, 0)
                self.drawCountryByCountryParam(country, red)
                self.hoverColoredCountries.remove(country)
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
        if arrowname == "arrow_right":
            self.getNextOption()
        elif arrowname == "arrow_left":
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
            indexCurrentOption = 0
            for correctOption in self.correctOptions:
                if correctOption in options:
                    options.remove(correctOption)
            if self.currentOption in options:
                indexCurrentOption = options.index(self.player0.currentOption)
            else:
                indexCurrentOption = len(options) // 2
            if indexCurrentOption + 1 >= len(options):
                self.currentOption = options[0]
            else:
                self.currentOption = options[indexCurrentOption + 1]
            self.displayOption()

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
            self.displayOption()

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
            indexCurrentOption = 0
            for correctOption in self.correctOptions:
                if correctOption in options:
                    options.remove(correctOption)
            if self.currentOption in options:
                indexCurrentOption = options.index(self.player0.currentOption)
            else:
                indexCurrentOption = len(options) // 2
            if indexCurrentOption <= 0:
                self.currentOption = options[len(options) - 1]
            else:
                self.currentOption = options[indexCurrentOption - 1]
            self.displayOption()
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
            self.displayOption()

    def drawAnOval(self, text):
        # circle

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        # draw circle
        # radius = 100
        # center = (1100, 500)
        # pygame.draw.circle(window, RED, center, radius)

        # draw oval

        rect = pygame.Rect(1000, 300, 200, 150)  # left, top, width, height
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

        y = rect.top + 70 - (len(lines) * 10)
        for line in lines:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(centerx=rect.centerx, y=y)
            self.window.blit(text_surface, text_rect)
            y += font.size(line)[1]

    def getCapital(self):
        capital = ""
        if self.isMultiplayer:
            capitalFile = open(f"countries\\{self.CONTINENT}\\{self.player0.currentOption}\\country.txt", "r")
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

    def getCountry(self):
        country = ""
        if self.isMultiplayer:
            countryFile = open(f"countries\\{self.CONTINENT}\\{self.player0.currentOption}\\country.txt", "r")
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

    def displayCapital(self):
        capital = self.getCapital()
        self.drawAnOval(capital)

    def displayCountry(self):
        country = self.getCountry()
        self.drawAnOval(country)

    def displayFlag(self):
        if self.isMultiplayer:
            option = pygame.image.load(f"countries\\{self.CONTINENT}\\{self.player0.currentOption}\\flag.png")
        else:
            option = pygame.image.load(f"countries\\{self.CONTINENT}\\{self.currentOption}\\flag.png")
        option = pygame.transform.scale(option, (130, 100))  # 130, 100 for flags
        self.window.blit(option, (1020, 200))  # 1020, 200 for flags

    def displayOption(self):
        if self.gameType == self.gameTypeFlags:
            self.displayFlag()
        if self.gameType == self.gameTypeCapitals:
            self.displayCapital()
        if self.gameType == self.gameTypeCountries:
            self.displayCountry()

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
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

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
                                   text_input="EUROPE", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            AFRICA_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550),
                                   text_input="AFRICA", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

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

    def playGame(self):
        # hand = HandTrackingModule.HandDetector()
        # hand.show()
        yellow = (238, 224, 29)
        green = (23, 165, 23)
        blue1 = (0, 51, 153)
        self.window.fill((255, 255, 255))
        bg_img = pygame.image.load(self.currentMap)
        bg_img = pygame.transform.scale(bg_img, (897, 680))
        self.window.blit(bg_img, (20, 20), )

        self.currentOption = self.getRandomOption()
        self.displayOption()

        arrow_right = pygame.image.load("arrow_right.png")
        arrow_right = pygame.transform.scale(arrow_right, (80, 65))
        self.window.blit(arrow_right, (1170, 215))

        arrow_left = pygame.image.load("arrow_left.png")
        arrow_left = pygame.transform.scale(arrow_left, (80, 65))
        self.window.blit(arrow_left, (920, 215))

        arrowColor = (34, 177, 76)
        runing = True

        while runing:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEMOTION:  # MOUSEBUTTONUP MOUSEMOTION
                    pos = pygame.mouse.get_pos()
                    self.undrawCountries(blue1)
                    self.drawCountry(pos[0], pos[1], blue1, yellow)
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.changeOptionIfArrowClicked(pos[0], pos[1])
                    self.displayOption()
                    self.drawCorrectCountry(pos[0], pos[1], yellow, green)

                    # initTreePixels()
                    # writeCountryPixelsInFile("Test", pos[0], pos[1])
            pygame.display.update()
        pygame.quit()

    def launch(self):
        pygame.init()
        pygame.display.set_caption("Menu")
        self.playGame()
        # main_menu()