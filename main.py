import HandTrackingModule
import HandTrackingModule as HTM
import numpy as np
import cv2.data
import pygame
import image
from fontTools.ttLib import TTFont

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def writeCountryPixelsInFile2(countryName, mousex, mousey):
    file = open(f"countries\\{countryName}\\pixels.txt", "w")
    margin = (0, 0, 0) # black
    uncolored = (0, 51, 153) # blue
    newColor = (238, 224, 29) # yellow
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
    # while not finished:



    # findMoreCountryPixels(file, window, mousex, mousey)
    # 
    # total = getUncoloredPixelsNeighboursFromSameCountry(window, mousex, mousey)
    # 
    # while total != ():
    #     totalList = list(total)
    #     length = len(totalList)
    #     xPixel = totalList[length // 2][0]
    #     yPixel = totalList[length // 2][1]
    #     findMoreCountryPixels(file, window, xPixel, yPixel)
    #     news = getUncoloredPixelsNeighboursFromSameCountry(window, xPixel, yPixel)
    #     for xPixel, yPixel in totalList:
    #         c = window.get_at((xPixel, yPixel))
    #         color = (c[0], c[1], c[2])
    #         if color == yellow:
    #             totalList.remove((xPixel, yPixel))
    #     totalNews = list(news)
    #     totalList += totalNews
    #     total = tuple(totalList)
    print("Finish")
    file.close()

def drawCountry(country, rgb):
    file = open(f"countries\\{country}\\pixels.txt", "r")
    pixels = file.readlines()
    for pixel in pixels:
        p = pixel.split()
        x = int(p[0])
        y = int(p[1])
        window.set_at((x, y), rgb)
        print(pixel)
    print("ok")


def findMoreCountryPixels(file, window, xPos, yPos):
    yellow = (238, 224, 29)
    red = (255, 255, 255)  # black
    white = (0, 0, 0)  # blue

    rightPos = xPos
    if rightPos < 0 or rightPos > SCREEN_WIDTH:
        return
    if yPos < 0 or yPos > SCREEN_HEIGHT:
        return
    c = window.get_at((rightPos + 1, yPos))
    colorNextRightYPos = (c[0], c[1], c[2])
    c = window.get_at((rightPos, yPos))
    colorRightYPos = (c[0], c[1], c[2])
    while colorRightYPos != red and colorNextRightYPos != yellow:
        up = yPos
        c = window.get_at((rightPos, up))
        colorRightUp = (c[0], c[1], c[2])
        while colorRightUp != red:
            window.set_at((rightPos, up), yellow)
            file.write(f"{rightPos} {up}\n")
            up = up + 1
            if up > SCREEN_HEIGHT:
                break
            print((rightPos, up))
            c = window.get_at((rightPos, up))
            colorRightUp = (c[0], c[1], c[2])
        down = yPos
        c = window.get_at((rightPos, down))
        colorRightDown = (c[0], c[1], c[2])
        while colorRightDown != red:
            window.set_at((rightPos, down), yellow)
            file.write(f"{rightPos} {down}\n")
            down = down - 1
            if down < 0:
                break
            c = window.get_at((rightPos, down))
            colorRightDown = (c[0], c[1], c[2])
        rightPos = rightPos + 1
        if rightPos > SCREEN_WIDTH:
            break
        c = window.get_at((rightPos, yPos))
        colorRightYPos = (c[0], c[1], c[2])

    leftPos = xPos
    c = window.get_at((leftPos - 1, yPos))
    colorNextLeftYPos = (c[0], c[1], c[2])
    c = window.get_at((leftPos, yPos))
    colorLeftYPos = (c[0], c[1], c[2])
    while colorLeftYPos != red and colorNextLeftYPos != yellow:
        up = yPos
        c = window.get_at((leftPos, up))
        colorLeftUp = (c[0], c[1], c[2])
        while colorLeftUp != red:
            window.set_at((leftPos, up), yellow)
            file.write(f"{leftPos} {up}\n")
            up = up + 1
            if up > SCREEN_HEIGHT:
                break
            c = window.get_at((leftPos, up))
            colorLeftUp = (c[0], c[1], c[2])
        down = yPos
        c = window.get_at((leftPos, down))
        colorLeftDown = (c[0], c[1], c[2])
        while colorLeftDown != red:
            window.set_at((leftPos, down), yellow)
            file.write(f"{leftPos} {down}\n")
            down = down - 1
            if down < 0:
                break
            c = window.get_at((leftPos, down))
            colorLeftDown = (c[0], c[1], c[2])
        leftPos = leftPos - 1
        if leftPos < 0:
            break
        c = window.get_at((leftPos, yPos))
        colorLeftYPos = (c[0], c[1], c[2])


def getUncoloredPixelsNeighboursFromSameCountry(window, xPos, yPos):
    yellow = (238, 224, 29)
    red = (255, 255, 255) #white
    white = (0, 51, 153)  # blue // culoarea initiala
    uncoloredPixels = ()

    rightPos = xPos
    if rightPos < 0 or rightPos > SCREEN_WIDTH:
        return uncoloredPixels
    if yPos < 0 or yPos > SCREEN_HEIGHT:
        return uncoloredPixels
    c = window.get_at((rightPos, yPos))
    colorRightYPos = (c[0], c[1], c[2])

    while colorRightYPos != red:
        up = yPos
        c = window.get_at((rightPos, up))
        colorRightUp = (c[0], c[1], c[2])
        while colorRightUp != red:
            # verify left neighbour
            if rightPos - 1 < 0:
                break
            c = window.get_at((rightPos - 1, up))
            colorLeftNeighbour = (c[0], c[1], c[2])
            if colorLeftNeighbour == white:
                uncoloredPixels += ((rightPos - 1, up),)

            # verify right neighbour
            if rightPos + 1 > SCREEN_WIDTH:
                break
            c = window.get_at((rightPos + 1, up))
            colorRightNeighbour = (c[0], c[1], c[2])
            if colorRightNeighbour == white:
                uncoloredPixels += ((rightPos + 1, up),)

            up = up + 1
            if up > SCREEN_HEIGHT:
                break
            c = window.get_at((rightPos, up))
            colorRightUp = (c[0], c[1], c[2])

        down = yPos
        c = window.get_at((rightPos, down))
        colorRightDown = (c[0], c[1], c[2])

        while colorRightDown != red:
            # verify left neighbour
            if rightPos - 1 < 0:
                break
            c = window.get_at((rightPos - 1, down))
            colorLeftNeighbour = (c[0], c[1], c[2])
            if colorLeftNeighbour == white:
                uncoloredPixels += ((rightPos - 1, down),)

            # verify right neighbour
            if rightPos + 1 > SCREEN_WIDTH:
                break
            c = window.get_at((rightPos + 1, down))
            colorRightNeighbour = (c[0], c[1], c[2])
            if colorRightNeighbour == white:
                uncoloredPixels += ((rightPos + 1, down),)
            down = down - 1
            if down < 0:
                break
            c = window.get_at((rightPos, down))
            colorRightDown = (c[0], c[1], c[2])

        rightPos = rightPos + 1
        if rightPos > SCREEN_WIDTH:
            break
        c = window.get_at((rightPos, yPos))
        colorRightYPos = (c[0], c[1], c[2])

    #####
    #####

    leftPos = xPos
    c = window.get_at((leftPos, yPos))
    colorLeftYPos = (c[0], c[1], c[2])
    while colorLeftYPos != red:
        up = yPos
        c = window.get_at((leftPos, up))
        colorLeftUp = (c[0], c[1], c[2])
        while colorLeftUp != red:
            # verify left neighbour
            if leftPos - 1 < 0:
                break
            c = window.get_at((leftPos - 1, up))
            colorLeftNeighbour = (c[0], c[1], c[2])
            if colorLeftNeighbour == white:
                uncoloredPixels += ((leftPos - 1, up),)

            # verify right neighbour
            c = window.get_at((leftPos + 1, up))
            if leftPos + 1 > SCREEN_WIDTH:
                break
            colorRightNeighbour = (c[0], c[1], c[2])
            if colorRightNeighbour == white:
                uncoloredPixels += ((leftPos + 1, up),)

            up = up + 1
            if up > SCREEN_HEIGHT:
                break
            c = window.get_at((leftPos, up))
            colorLeftUp = (c[0], c[1], c[2])

        down = yPos
        c = window.get_at((leftPos, down))
        colorLeftDown = (c[0], c[1], c[2])

        while colorLeftDown != red:
            # verify left neighbour
            if leftPos - 1 < 0:
                break
            c = window.get_at((leftPos - 1, down))
            colorLeftNeighbour = (c[0], c[1], c[2])
            if colorLeftNeighbour == white:
                uncoloredPixels += ((leftPos - 1, down),)

            # verify right neighbour
            if leftPos + 1 > SCREEN_WIDTH:
                break
            c = window.get_at((leftPos + 1, down))
            colorRightNeighbour = (c[0], c[1], c[2])
            if colorRightNeighbour == white:
                uncoloredPixels += ((leftPos + 1, down),)

            down = down - 1
            if down < 0:
                break
            c = window.get_at((leftPos, down))
            colorLeftDown = (c[0], c[1], c[2])

        leftPos = leftPos - 1
        if leftPos < 0:
            break
        c = window.get_at((leftPos, yPos))
        colorLeftYPos = (c[0], c[1], c[2])
    return uncoloredPixels


def writeCountryPixelsInFile(countryName, mousex, mousey):
    file = open(f"countries\\{countryName}\\pixels.txt", "w")

    findMoreCountryPixels(file, window, mousex, mousey)

    total = getUncoloredPixelsNeighboursFromSameCountry(window, mousex, mousey)

    while total != ():
        totalList = list(total)
        length = len(totalList)
        xPixel = totalList[length // 2][0]
        yPixel = totalList[length // 2][1]
        findMoreCountryPixels(file, window, xPixel, yPixel)
        news = getUncoloredPixelsNeighboursFromSameCountry(window, xPixel, yPixel)
        for xPixel, yPixel in totalList:
            c = window.get_at((xPixel, yPixel))
            color = (c[0], c[1], c[2])
            if color == yellow:
                totalList.remove((xPixel, yPixel))
        totalNews = list(news)
        totalList += totalNews
        total = tuple(totalList)
    print("Finish")
    file.close()


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
    blue1 = (0, 0, 128)
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
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # window.blit(text, (1020, 500))
                # c = window.get_at((pos[0], pos[1]))
                # print((c[0], c[1], c[2]))
                # writeCountryPixelsInFile2("Romania", pos[0], pos[1])
                # file = open("countries\\Romania\\pixels.txt", "w")
                # findMoreCountryPixels(file, window, pos[0], pos[1])
                drawCountry("Rusia", yellow)
        pygame.display.update()
    pygame.quit()
