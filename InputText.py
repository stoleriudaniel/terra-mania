import pygame


class InputText:
    def __init__(self, x, y, width, height, font=None, font_size=30, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = ''
        self.font = pygame.font.SysFont(font, font_size)
        self.surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the active variable
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Clear the input text when the user presses enter
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character when the user presses backspace
                    self.text = self.text[:-1]
                else:
                    # Add the pressed character to the text
                    self.text += event.unicode
                # Update the text surface
                self.surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Update the text surface every frame
        self.surface = self.font.render(self.text, True, self.color)

    def draw(self, surface):
        # Draw the text input on the surface
        pygame.draw.rect(surface, self.color, self.rect, 2)
        surface.blit(self.surface, (self.rect.x + 5, self.rect.y + 5))
