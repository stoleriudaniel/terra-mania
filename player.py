class Player():
    def __init__(self, startx, starty, playerid):
        self.id = playerid
        self.x = startx
        self.y = starty
        self.click = 0
        self.currentOption = "no option"
        self.currentHoveredCountry = ""
        self.lastCorrectOption = "none"
        self.hoverColoredCountries = []

        self.correctCountries = []
        self.correctFlags = []
        self.correctCapitals = []

        self.correctOptions = []

        self.incorrectCountries = []

    def move(self, xCood, yCoord):
        self.x = xCood
        self.y = yCoord