class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.font = font
        self.baseColor, self.hoveringColor = base_color, hovering_color
        self.textInput = text_input
        self.text = self.font.render(self.textInput, True, self.baseColor)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))
        self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)
