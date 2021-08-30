import pygame


class Points:
    def __init__(self, font, size, color, screen):
        self.font_name = font
        self.font_size = size
        self.font_color = color
        self.screen = screen
        self.points = 0

    def write_points(self):
        out_font = pygame.font.Font(self.font_name, self.font_size)
        text_surface = out_font.render(str(self.points), True, self.font_color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen.get_width() / 2
        text_rect.top = 10
        self.screen.blit(text_surface, text_rect)

    def add_point(self, point):
        self.points += point

    