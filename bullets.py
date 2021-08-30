import pygame
from pygame import Surface
from pygame.sprite import Sprite
# from pygame.key import get_pressed


# 繼承 pygame 內建的 Sprite 類別
class Bullets(Sprite):
    def __init__(self, COLOR, WIDTH, HEIGHT, player_x, player_y, img):
        Sprite.__init__(self)    # Call the parent class (Sprite) constructor
        self.width = WIDTH       # 遊戲視窗的寬度
        self.height = HEIGHT     # 遊戲視窗的長度
        self.color = COLOR       # (255,255,0)
        self.speed_y = -5       # 控制子彈的速度
        self.image = pygame.transform.scale(img,(8,25))
        self.image.set_colorkey(self.color)       
        # self.image = Surface([10, 20]) # [width, height]
        # self.image.fill(self.color)


        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = player_x, player_y
        # self.rect.centerx = player_x
        # self.rect.bottom = player_y

    def update(self):
        self.auto_move()
        self.out_screen()

    # 控制移動
    def auto_move(self):
        self.rect.y += self.speed_y
    
    # 清除超出視窗外的物件
    def out_screen(self):
        if self.rect.bottom <= 0:    
            self.kill()




