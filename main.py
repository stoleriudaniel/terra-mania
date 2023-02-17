import os
from pathlib import Path

import HandTrackingModule
import HandTrackingModule as HTM
import numpy as np
import cv2.data
import pygame
import image
from fontTools.ttLib import TTFont

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

coloredCountries = []

def initTreePixels():
    directories = [x[0] for x in os.walk('countries')]
    print(directories)
    countries = []
    for index in range(0, len(directories)):
        country = directories[index].split("\\")
        if len(country) > 1:
            path = Path(f"countries\\{country[1]}\\pixels.txt")
            if not path.is_file():
                continue
            pixelsFile = open(f"countries\\{country[1]}\\pixels.txt", "r")
            rows = pixelsFile.readlines()
            print(country[1])
            for row in rows:
                result = row.split()
                xCord = result[0]
                yCord = result[1]
                filename = int(xCord) // 100 * 100
                file = open(f"tree\\pixels\\{filename}.txt", "a")
                file.write(f"{xCord} {yCord} {country[1]}\n")
    print("Finish")


def writeCountryPixelsInFile(countryName, mousex, mousey):
    file = open(f"countries\\{countryName}\\pixels.txt", "w")
    margin = (0, 0, 0)  # black
    uncolored = (0, 51, 153)  # blue
    newColor = (238, 224, 29)  # yellow
    finished = False
    uncoloredPixelsList = []
    print(mousex, mousey)
    c = window.get_at((mousex, mousey))
    if (c[0], c[1], c[2]) == uncolored:
        uncoloredPixelsList.append((mousex, mousey))
    print(uncoloredPixelsList)
    while uncoloredPixelsList:
        currentPixel = uncoloredPixelsList.pop(0)
        print(currentPixel[0])
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
    c = window.get_at((mouseX, mouseY))
    # print((c[0], c[1], c[2]) != initRgb, c)
    if (c[0], c[1], c[2]) != initRgb:
        return
    country = ""
    treeFilename = mouseX // 100 * 100
    treeFile = open(f"tree\\pixels\\{treeFilename}.txt", "r")
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
    drawCountryByCountryParam(country, newRgb)
    coloredCountries.append(country)
    print("ok")


def undrawCountries(newRGB):
    for country in coloredCountries:
        drawCountryByCountryParam(country, newRGB)
        coloredCountries.remove(country)

def drawCountryByCountryParam(country, newRGB):
    countryPixelsFile = open(f"countries\\{country}\\pixels.txt", "r")
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


if __name__ == '__main__':
    # hand = HandTrackingModule.HandDetector()
    # hand.show()
    yellow = (238, 224, 29)
    red = (255, 255, 255)  # white
    white = (0, 0, 0)  # blue
    green = (23, 165, 23)
    green1 = (0, 255, 0)
    blue1 = (0, 51, 153)
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    window.fill((255, 255, 255))
    bg_img = pygame.image.load('Europe_map1.png')
    bg_img = pygame.transform.scale(bg_img, (897, 680))
    window.blit(bg_img, (20, 20), )

    flag = pygame.image.load("Flags\\Romania_flag.png")
    flag = pygame.transform.scale(flag, (130, 100))
    window.blit(flag, (1020, 200))

    # Font = pygame.font.Font("fonts\\freedom-font\\Freedom-10eM.ttf", 32)
    # print(Font)
    # # Font = pygame.font.SysFont('timesnewroman', 30)
    # text = Font.render('GeeksForGeeks', False, green1, blue1)

    runing = True
    while runing:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEMOTION: # MOUSEBUTTONUP MOUSEMOTION
                pos = pygame.mouse.get_pos()
                print([pos[0], pos[1]])
                if len(coloredCountries)>0:
                    undrawCountries(blue1)
                # writeCountryPixelsInFile("Test", pos[0], pos[1])
                drawCountry(pos[0], pos[1], blue1, yellow)
                # initTreePixels()
                # drawCountryByCountryParam("Macedonia", yellow)

        pygame.display.update()
    pygame.quit()
