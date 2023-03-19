class Player():
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty

    def move(self, xCood, yCoord):
        self.x = xCood
        self.y = yCoord