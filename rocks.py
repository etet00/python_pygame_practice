from random import randrange
import pygame
from pygame.sprite import Sprite


# 繼承 pygame 內建的 Sprite 類別
class Rocks(Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, COLOR, WIDTH, HEIGHT, img):
        Sprite.__init__(self)    # Call the parent class (Sprite) constructor
        self.width = WIDTH       # 遊戲視窗的寬度
        self.height = HEIGHT     # 遊戲視窗的長度
        self.color = COLOR
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # self.image = Surface([50, 40]) # [width, height]
        # self.image.fill(self.color)
        self.w_pixal = randrange(10,100)
        self.h_pixal = self.w_pixal + randrange(-5,5)
        self.image_ori = pygame.transform.scale(img,(self.w_pixal,self.h_pixal))
        self.image_ori.set_colorkey(self.color)
        self.image = self.image_ori.copy()

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width / 2) * 0.60
        # pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)  # 測適用

        self.rect.x, self.rect.y = self.rand_location()
        self.speed_x, self.speed_y = self.rand_speed()

        self.total_degree = 0
        self.degree = self.rand_degree()
    
    def update(self):
        self.rotate()
        self.auto_move()
        self.out_screen()

    def auto_move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def out_screen(self):
        if self.rect.top >= self.height or self.rect.left >= self.width or self.rect.right <= 0:    
            self.rect.x, self.rect.y = self.rand_location()
            self.speed_x, self.speed_y = self.rand_speed()

    def rand_location(self):
        x = randrange(0, self.width- self.rect.width)
        y = randrange(-150, -130)
        return x, y

    def rand_speed(self):
        return randrange(-3, 3), randrange(1, 8)

    def rand_degree(self):
        return randrange(-3,3)

    def rotate(self):
        self.total_degree += self.degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center