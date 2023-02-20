import os
from pathlib import Path
from button import Button

import HandTrackingModule
import HandTrackingModule as HTM
import numpy as np
import cv2.data
import pygame, sys
import image
from fontTools.ttLib import TTFont

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

hoverColoredCountries = []
correctCountries = []
correctFlags = []
incorrectCountries = []
currentFlag = ""
currentCountry = ""

CONTINENT = "North-America"


def initTreePixels():
    print("In initTreePixels")
    directories = [x[0] for x in os.walk(f"countries\\{CONTINENT}")]
    countries = []
    print(directories)
    for index in range(0, len(directories)):
        country = directories[index].split("\\")
        if len(country) > 2:
            path = Path(f"countries\\{CONTINENT}\\{country[2]}\\pixels.txt")
            if not path.is_file():
                continue
            print("country: ", country[2])
            pixelsFile = open(f"countries\\{CONTINENT}\\{country[2]}\\pixels.txt", "r")
            rows = pixelsFile.readlines()
            for row in rows:
                result = row.split()
                xCord = result[0]
                yCord = result[1]
                filename = int(xCord) // 100 * 100
                file = open(f"tree\\countries\\{CONTINENT}\\pixels\\{filename}.txt", "a")
                file.write(f"{xCord} {yCord} {country[2]}\n")
    print("Finish")


def writeCountryPixelsInFile(countryName, mousex, mousey):
    file = open(f"countries\\{countryName}\\pixels.txt", "w")
    # file = open(f"arrows\\{countryName}\\pixels.txt", "w")
    margin = (0, 0, 0)  # black
    uncolored = (0, 51, 153)  # blue
    newColor = (238, 224, 29)  # yellow
    arrowColor = (34, 177, 76)
    # uncolored = arrowColor
    finished = False
    uncoloredPixelsList = []
    c = window.get_at((mousex, mousey))
    if (c[0], c[1], c[2]) == uncolored:
        uncoloredPixelsList.append((mousex, mousey))
    while uncoloredPixelsList:
        currentPixel = uncoloredPixelsList.pop(0)
        file.write(f"{currentPixel[0]} {currentPixel[1]}\n")
        window.set_at((currentPixel[0], currentPixel[1]), newColor)
        c1 = window.get_at((currentPixel[0] - 1, currentPixel[1] + 1))
        c2 = window.get_at((currentPixel[0], currentPixel[1] + 1))
        c3 = window.get_at((currentPixel[0] + 1, currentPixel[1] + 1))
        c4 = window.get_at((currentPixel[0] + 1, currentPixel[1]))
        c5 = window.get_at((currentPixel[0] + 1, currentPixel[1] - 1))
        c6 = window.get_at((currentPixel[0], currentPixel[1] - 1))
        c7 = window.get_at((currentPixel[0] - 1, currentPixel[1] - 1))
        c8 = window.get_at((currentPixel[0] - 1, currentPixel[1]))
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


def drawCountry(mouseX, mouseY, initRgb, newRgb):
    red = (255, 0, 0)
    country = ""
    c = window.get_at((mouseX, mouseY))
    # print((c[0], c[1], c[2]) != initRgb, c)
    if (c[0], c[1], c[2]) != initRgb:
        if (c[0], c[1], c[2]) != red:
            globals()['currentCountry'] = country
        return
    treeFilename = mouseX // 100 * 100
    treeFile = open(f"tree\\countries\\{CONTINENT}\\pixels\\{treeFilename}.txt", "r")
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
    globals()['currentCountry'] = country
    drawCountryByCountryParam(country, newRgb)
    hoverColoredCountries.append(country)


def drawCorrectCountry(mouseX, mouseY, initRgb, newRgb):
    c = window.get_at((mouseX, mouseY))
    # print((c[0], c[1], c[2]) != initRgb, c)
    if (c[0], c[1], c[2]) != initRgb:
        return
    country = ""
    treeFilename = mouseX // 100 * 100
    treeFile = open(f"tree\\countries\\{CONTINENT}\\pixels\\{treeFilename}.txt", "r")
    rows = treeFile.readlines()
    for row in rows:
        result = row.split()
        xCord = result[0]
        yCord = result[1]
        if int(xCord) == mouseX and int(yCord) == mouseY:
            country = result[2]
            break
    print(country)
    if country == "":
        return
    print(f"{country}_flag.png", globals()['currentFlag'])
    if f"{country}_flag.png" == globals()['currentFlag']:
        print("country is correct")
        drawCountryByCountryParam(country, newRgb)
        hoverColoredCountries.remove(country)
        correctFlags.append(f"{country}_flag.png")
        getNextFlag()
    else:
        incorrectCountries.append(country)
        red = (255, 0, 0)
        drawCountryByCountryParam(country, red)
        hoverColoredCountries.remove(country)
    # hoverColoredCountries.append(country)
    print("ok")


def undrawCountries(newRGB):
    for incorrectCountry in incorrectCountries:
        if incorrectCountry != globals()['currentCountry']:
            hoverColoredCountries.append(incorrectCountry)
            incorrectCountries.remove(incorrectCountry)
    for country in hoverColoredCountries:
        drawCountryByCountryParam(country, newRGB)
        hoverColoredCountries.remove(country)
    print("curr:", globals()['currentCountry'])
    print("inc:", incorrectCountries)

def drawCountryByCountryParam(country, newRGB):
    countryPixelsFile = open(f"countries\\{CONTINENT}\\{country}\\pixels.txt", "r")
    countryPixels = countryPixelsFile.readlines()
    for pixel in countryPixels:
        p = pixel.split()
        x = int(p[0])
        y = int(p[1])
        window.set_at((x, y), newRGB)

def initColors():
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
                drawCountry(initRGBCountry, (r, g, b))

def changeFlagIfArrowClicked(mouseX, mouseY):
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
        getNextFlag()
    elif arrowname == "arrow_left":
        getPreviousFlag()

def getNextFlag():
    flags = []
    for x in os.walk(f"flags\\{CONTINENT}"):
        flags = x[2]
    if len(flags) == 0:
        return
    indexCurrentFlag = 0
    for correctFlag in correctFlags:
        if correctFlag in flags:
            flags.remove(correctFlag)
    if currentFlag in flags:
        indexCurrentFlag = flags.index(currentFlag)
    else:
        indexCurrentFlag = len(flags) // 2
    if indexCurrentFlag + 1 >= len(flags):
        globals()['currentFlag'] = flags[0]
    else:
        globals()['currentFlag'] = flags[indexCurrentFlag + 1]
    displayFlag()

def getPreviousFlag():
    flags = []
    for x in os.walk(f"flags\\{CONTINENT}"):
        flags = x[2]
    if len(flags) == 0:
        return
    indexCurrentFlag = 0
    for correctFlag in correctFlags:
        if correctFlag in flags:
            flags.remove(correctFlag)
    if currentFlag in flags:
        indexCurrentFlag = flags.index(currentFlag)
    else:
        indexCurrentFlag = len(flags) // 2
    if indexCurrentFlag <= 0:
        print("hello3: ", flags[len(flags) - 1])
        globals()['currentFlag'] = flags[len(flags) - 1]
    else:
        print("hello4", flags[indexCurrentFlag - 1])
        globals()['currentFlag'] = flags[indexCurrentFlag - 1]
    displayFlag()

def displayFlag():
    flag = pygame.image.load(f"Flags\\{CONTINENT}\\{currentFlag}")
    flag = pygame.transform.scale(flag, (130, 100))
    window.blit(flag, (1020, 200))


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    playGameEurope()
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


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # play()
                    continentsMenu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def continentsMenu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        EUROPE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="EUROPE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        AFRICA_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550),
                             text_input="AFRICA", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [EUROPE_BUTTON, AFRICA_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EUROPE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playGameEurope()
                if AFRICA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playGameEurope()

        pygame.display.update()

def playGameEurope():
    # hand = HandTrackingModule.HandDetector()
    # hand.show()
    yellow = (238, 224, 29)
    green = (23, 165, 23)
    blue1 = (0, 51, 153)
    window.fill((255, 255, 255))
    bg_img = pygame.image.load('Europe_map1.png')
    # bg_img = pygame.image.load('south_america.png')
    bg_img = pygame.transform.scale(bg_img, (897, 680))
    window.blit(bg_img, (20, 20), )

    globals()['currentFlag'] = "Germany_flag.png"
    displayFlag()

    arrow_right = pygame.image.load("arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, (80, 65))
    window.blit(arrow_right, (1170, 215))

    arrow_left = pygame.image.load("arrow_left.png")
    arrow_left = pygame.transform.scale(arrow_left, (80, 65))
    window.blit(arrow_left, (920, 215))

    arrowColor = (34, 177, 76)
    runing = True
    while runing:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEMOTION: # MOUSEBUTTONUP MOUSEMOTION
                pos = pygame.mouse.get_pos()
                undrawCountries(blue1)
                drawCountry(pos[0], pos[1], blue1, yellow)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print("click:", [pos[0], pos[1]])
                changeFlagIfArrowClicked(pos[0], pos[1])
                displayFlag()
                drawCorrectCountry(pos[0], pos[1], yellow, green)
                print(hoverColoredCountries)
        pygame.display.update()
    pygame.quit()

def playGameSouthAmerica():
    # hand = HandTrackingModule.HandDetector()
    # hand.show()
    yellow = (238, 224, 29)
    green = (23, 165, 23)
    blue1 = (0, 51, 153)
    window.fill((255, 255, 255))
    bg_img = pygame.image.load('south_america112.png')
    # bg_img = pygame.image.load('south_america.png')
    bg_img = pygame.transform.scale(bg_img, (897, 680))
    window.blit(bg_img, (20, 20), )

    globals()['currentFlag'] = "Venezuela_flag.png"
    displayFlag()

    arrow_right = pygame.image.load("arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, (80, 65))
    window.blit(arrow_right, (1170, 215))

    arrow_left = pygame.image.load("arrow_left.png")
    arrow_left = pygame.transform.scale(arrow_left, (80, 65))
    window.blit(arrow_left, (920, 215))

    arrowColor = (34, 177, 76)
    runing = True
    while runing:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEMOTION: # MOUSEBUTTONUP MOUSEMOTION
                pos = pygame.mouse.get_pos()
                undrawCountries(blue1)
                drawCountry(pos[0], pos[1], blue1, yellow)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print("click:", [pos[0], pos[1]])
                changeFlagIfArrowClicked(pos[0], pos[1])
                displayFlag()
                drawCorrectCountry(pos[0], pos[1], yellow, green)
                print(hoverColoredCountries)

                # initTreePixels()
                # writeCountryPixelsInFile("Test", pos[0], pos[1])
        pygame.display.update()
    pygame.quit()

def playGameNorthAmerica():
    # hand = HandTrackingModule.HandDetector()
    # hand.show()
    yellow = (238, 224, 29)
    green = (23, 165, 23)
    blue1 = (0, 51, 153)
    window.fill((255, 255, 255))
    bg_img = pygame.image.load('north-america111.png')
    # bg_img = pygame.image.load('south_america.png')
    bg_img = pygame.transform.scale(bg_img, (897, 680))
    window.blit(bg_img, (20, 20), )

    globals()['currentFlag'] = "Bahamas_flag.png"
    displayFlag()

    arrow_right = pygame.image.load("arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, (80, 65))
    window.blit(arrow_right, (1170, 215))

    arrow_left = pygame.image.load("arrow_left.png")
    arrow_left = pygame.transform.scale(arrow_left, (80, 65))
    window.blit(arrow_left, (920, 215))

    arrowColor = (34, 177, 76)
    runing = True
    while runing:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEMOTION: # MOUSEBUTTONUP MOUSEMOTION
                pos = pygame.mouse.get_pos()
                # undrawCountries(blue1)
                # drawCountry(pos[0], pos[1], blue1, yellow)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print("click:", [pos[0], pos[1]])
                # changeFlagIfArrowClicked(pos[0], pos[1])
                # displayFlag()
                # drawCorrectCountry(pos[0], pos[1], yellow, green)
                # print(hoverColoredCountries)

                # initTreePixels()
                writeCountryPixelsInFile("Test", pos[0], pos[1])
        pygame.display.update()
    pygame.quit()

def playGameAsia():
    # hand = HandTrackingModule.HandDetector()
    # hand.show()
    yellow = (238, 224, 29)
    green = (23, 165, 23)
    blue1 = (0, 51, 153)
    window.fill((255, 255, 255))
    bg_img = pygame.image.load('asia112.png')
    # bg_img = pygame.image.load('south_america.png')
    bg_img = pygame.transform.scale(bg_img, (897, 680))
    window.blit(bg_img, (20, 20), )

    globals()['currentFlag'] = "Japan_flag.png"
    displayFlag()

    arrow_right = pygame.image.load("arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, (80, 65))
    window.blit(arrow_right, (1170, 215))

    arrow_left = pygame.image.load("arrow_left.png")
    arrow_left = pygame.transform.scale(arrow_left, (80, 65))
    window.blit(arrow_left, (920, 215))

    arrowColor = (34, 177, 76)
    runing = True
    while runing:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEMOTION: # MOUSEBUTTONUP MOUSEMOTION
                pos = pygame.mouse.get_pos()
                # undrawCountries(blue1)
                # drawCountry(pos[0], pos[1], blue1, yellow)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print("click:", [pos[0], pos[1]])
                # changeFlagIfArrowClicked(pos[0], pos[1])
                # displayFlag()
                # drawCorrectCountry(pos[0], pos[1], yellow, green)
                # print(hoverColoredCountries)

                # initTreePixels()
                writeCountryPixelsInFile("Test", pos[0], pos[1])
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("assets/Background.png")

    # playGameSouthAmerica()
    # playGameEurope()
    # playGameAsia()
    playGameNorthAmerica()

    # main_menu()